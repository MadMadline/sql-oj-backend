import time
import docker
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from psycopg2.errors import QueryCanceled
from contextlib import closing

DOCKER_IMAGE = "postgres:15-alpine"
DB_NAME = "judge_db"
DB_USER = "judge_user"
DB_PASSWORD = "judge_pass"
CONTAINER_TIMEOUT = 60            # 适当加长
SQL_TIMEOUT = 30
MEM_LIMIT = "512m"

app = FastAPI(title="SQL Judge Service", version="1.0.0")
docker_client = docker.from_env()

class TestCase(BaseModel):
    expected_output: str
    test_input: Optional[str] = ""

class JudgeRequest(BaseModel):
    submitted_sql: str
    test_cases: List[TestCase]
    create_table_sql: Optional[str] = ""
    timeout: Optional[int] = SQL_TIMEOUT

class TestCaseResult(BaseModel):
    test_case_id: int
    passed: bool
    actual_output: str
    error_message: Optional[str] = None

class JudgeResponse(BaseModel):
    passed: bool
    execution_status: str
    score: int
    details: List[TestCaseResult]

def wait_for_db(container, timeout=CONTAINER_TIMEOUT):
    """等待容器启动并返回 (host, port)"""
    start = time.time()
    while time.time() - start < timeout:
        container.reload()
        ports = container.attrs['NetworkSettings']['Ports']
        host_port = None
        for container_port, host_bindings in ports.items():
            if container_port == '5432/tcp' and host_bindings:
                host_port = host_bindings[0]['HostPort']
                break
        if not host_port:
            time.sleep(0.5)
            continue
        try:
            conn = psycopg2.connect(
                host='127.0.0.1', port=host_port, database=DB_NAME,
                user=DB_USER, password=DB_PASSWORD, connect_timeout=2
            )
            conn.close()
            return '127.0.0.1', host_port
        except Exception:
            time.sleep(0.5)
    raise TimeoutError("PostgreSQL 容器启动超时")

def run_sql_on_container(host, port, sql, timeout):
    conn = psycopg2.connect(
        host=host, port=port, database=DB_NAME,
        user=DB_USER, password=DB_PASSWORD, connect_timeout=timeout
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(f"SET statement_timeout = {timeout * 1000};")
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        last_result = None
        for stmt in statements:
            cur.execute(stmt)
            if cur.description:
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                last_result = {"columns": columns, "rows": rows}
            else:
                last_result = {"columns": [], "rows": [], "message": "SQL executed successfully"}
        return last_result if last_result is not None else {"columns": [], "rows": []}
    finally:
        cur.close()
        conn.close()

def format_result_set(result: Dict) -> str:
    columns = result.get("columns", [])
    rows = result.get("rows", [])
    if not columns:
        return ""
    header = "|".join(str(c) for c in columns)
    lines = [header]
    for row in rows:
        line = "|".join(str(v) if v is not None else "" for v in row)
        lines.append(line)
    return "\n".join(lines)

def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines()).strip()

def compare_output(actual: str, expected: str) -> bool:
    return normalize_output(actual) == normalize_output(expected)

def create_judge_container():
    container = docker_client.containers.run(
        DOCKER_IMAGE,
        environment={
            "POSTGRES_DB": DB_NAME,
            "POSTGRES_USER": DB_USER,
            "POSTGRES_PASSWORD": DB_PASSWORD
        },
        ports={'5432/tcp': None},
        detach=True,
        remove=True,
        tmpfs={
            "/var/lib/postgresql/data": "rw,noexec,nosuid,size=256m",
            "/var/run/postgresql": "rw,noexec,nosuid,size=16m",
            "/tmp": "rw,noexec,nosuid,size=64m",
            "/dev/shm": "rw,noexec,nosuid,size=64m"
        },
        mem_limit=MEM_LIMIT,
        cpu_period=100000,
        cpu_quota=50000,
        cap_add=["CHOWN", "SETUID", "SETGID", "DAC_OVERRIDE"],
        cap_drop=["SYS_ADMIN", "NET_RAW", "SYS_MODULE", "AUDIT_WRITE", "MKNOD"],
        security_opt=["no-new-privileges:true"]
    )
    return container

@app.post("/judge", response_model=JudgeResponse)
async def judge(request: JudgeRequest):
    container = None
    try:
        container = create_judge_container()
        host, port = wait_for_db(container)

        if request.create_table_sql and request.create_table_sql.strip():
            run_sql_on_container(host, port, request.create_table_sql, request.timeout)

        details = []
        passed_count = 0

        for idx, tc in enumerate(request.test_cases):
            try:
                with closing(psycopg2.connect(
                    host=host, port=port, database=DB_NAME,
                    user=DB_USER, password=DB_PASSWORD,
                    connect_timeout=request.timeout
                )) as conn:
                    conn.autocommit = False
                    with conn.cursor() as cur:
                        cur.execute(f"SET statement_timeout = {request.timeout * 1000};")
                        if tc.test_input and tc.test_input.strip():
                            for stmt in [s.strip() for s in tc.test_input.split(';') if s.strip()]:
                                cur.execute(stmt)
                        cur.execute(request.submitted_sql)
                        if cur.description:
                            rows = cur.fetchall()
                            columns = [desc[0] for desc in cur.description]
                            result_dict = {"columns": columns, "rows": rows}
                        else:
                            result_dict = {"columns": [], "rows": []}
                        conn.rollback()

                        actual_output = format_result_set(result_dict)
                        is_pass = compare_output(actual_output, tc.expected_output)
                        if is_pass:
                            passed_count += 1

                        details.append(TestCaseResult(
                            test_case_id=idx,
                            passed=is_pass,
                            actual_output=actual_output
                        ))
            except QueryCanceled:
                details.append(TestCaseResult(
                    test_case_id=idx,
                    passed=False,
                    actual_output="",
                    error_message="SQL执行超时"
                ))
            except Exception as e:
                import traceback
                traceback.print_exc()
                details.append(TestCaseResult(
                    test_case_id=idx,
                    passed=False,
                    actual_output="",
                    error_message=str(e)
                ))

        total = len(request.test_cases)
        score = int(passed_count / total * 100) if total > 0 else 0
        all_passed = (passed_count == total)

        return JudgeResponse(
            passed=all_passed,
            execution_status="ACCEPTED" if all_passed else "WRONG_ANSWER",
            score=score,
            details=details
        )

    except TimeoutError:
        return JudgeResponse(
            passed=False,
            execution_status="TIMEOUT",
            score=0,
            details=[]
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JudgeResponse(
            passed=False,
            execution_status="ERROR",
            score=0,
            details=[]
        )
    finally:
        if container:
            try:
                container.stop()
            except:
                pass

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)