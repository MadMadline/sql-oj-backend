from django.utils import timezone
from django.db.models import Count, Q, Avg, Max, Sum
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Submission
from .serializers import SubmissionSerializer
from .judge import judge_submission
from apps.questions.models import Question
from apps.exams.models import Exam
from apps.users.models import User
from apps.users.permissions import IsTeacher


class SubmissionViewSet(viewsets.ModelViewSet):
    """提交与判题 ViewSet"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.user_type == 'student':
            qs = qs.filter(student=self.request.user)
        elif self.request.user.user_type == 'teacher':
            qs = qs.filter(student__teacher=self.request.user)
        return qs

    @action(detail=False, methods=['post'])
    def submit(self, request):
        """学生提交 SQL 并触发判题"""
        question_id = request.data.get('question_id')
        exam_id = request.data.get('exam_id')
        submitted_sql = request.data.get('submitted_sql')

        if not question_id or not submitted_sql:
            return Response(
                {'error': 'question_id 和 submitted_sql 为必填'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 考试模式下校验时间
        if exam_id:
            try:
                exam = Exam.objects.get(id=exam_id)
            except Exam.DoesNotExist:
                return Response({'error': '考试不存在'}, status=status.HTTP_404_NOT_FOUND)
            now = timezone.now()
            if not (exam.start_time <= now <= exam.end_time):
                return Response(
                    {'error': '不在考试时间内'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 获取题目和测试用例
        try:
            question = Question.objects.prefetch_related('test_cases').get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': '题目不存在'}, status=status.HTTP_404_NOT_FOUND)

        test_cases = list(
            question.test_cases.values('test_input', 'expected_output')
        )

        # 调用判题服务
        result = judge_submission(
            submitted_sql,
            test_cases,
            question.create_table_sql or ''
        )

        # 保存提交记录
        submission = Submission.objects.create(
            student=request.user,
            question=question,
            exam_id=exam_id,
            submitted_sql=submitted_sql,
            execution_status=result.get('execution_status', ''),
            score=result.get('score', 0),
        )

        return Response(
            SubmissionSerializer(submission).data,
            status=status.HTTP_201_CREATED
        )


class StatsViewSet(viewsets.ViewSet):
    """统计分析 ViewSet"""
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """整体概览"""
        total_questions = Question.objects.count()
        total_submissions = Submission.objects.count()
        total_users = User.objects.count()
        return Response({
            'total_questions': total_questions,
            'total_submissions': total_submissions,
            'total_users': total_users,
        })

    @action(detail=False, methods=['get'])
    def questions(self, request):
        """每题完成率（教师可见）"""
        if request.user.user_type != 'teacher':
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        stats = []
        for q in Question.objects.all():
            total = Submission.objects.filter(question=q).count()
            passed = Submission.objects.filter(
                question=q, execution_status='ACCEPTED'
            ).count()
            stats.append({
                'question_id': q.id,
                'title': q.title,
                'total_submissions': total,
                'passed': passed,
                'rate': round(passed / total, 2) if total else 0,
            })
        return Response(stats)

    @action(detail=False, methods=['get'])
    def students(self, request):
        """学生通过率排名（教师可见）"""
        if request.user.user_type != 'teacher':
            return Response({'error': '无权限'}, status=status.HTTP_403_FORBIDDEN)

        students = User.objects.filter(user_type='student')
        stats = []
        for s in students:
            total = Submission.objects.filter(student=s).count()
            passed = Submission.objects.filter(
                student=s, execution_status='ACCEPTED'
            ).count()
            stats.append({
                'student_id': s.id,
                'username': s.username,
                'total_submissions': total,
                'passed': passed,
                'rate': round(passed / total, 2) if total else 0,
            })
        stats.sort(key=lambda x: x['rate'], reverse=True)
        return Response(stats)
