from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Exam, ExamQuestion
from .serializers import ExamSerializer, ExamQuestionSerializer
from apps.users.permissions import IsTeacher
from apps.users.models import User
from apps.questions.models import Question


class ExamViewSet(viewsets.ModelViewSet):
    """考试管理 ViewSet"""
    serializer_class = ExamSerializer

    def get_queryset(self):
        user = self.request.user
        base_qs = Exam.objects.all().prefetch_related(
            'exam_questions__question', 'students'
        )
        if user.user_type == 'teacher':
            # 教师只看自己创建的考试
            return base_qs.filter(teacher=user)
        # 学生：全部开放的 + 自己被指定的
        return base_qs.filter(
            Q(student_scope='all') | Q(students=user)
        ).distinct()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def _validate_question_ids(self, questions_data):
        """验证 exam_questions 中的题目ID是否合法"""
        if not questions_data:
            return None
        question_ids = [q.get('question') for q in questions_data if q.get('question')]
        existing_ids = set(
            Question.objects.filter(id__in=question_ids).values_list('id', flat=True)
        )
        invalid_ids = [qid for qid in question_ids if qid not in existing_ids]
        if invalid_ids:
            return invalid_ids
        return None

    def perform_create(self, serializer):
        # 验证题目ID
        questions_data = self.request.data.get('exam_questions', [])
        invalid_ids = self._validate_question_ids(questions_data)
        if invalid_ids:
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                {'exam_questions': f'以下题目ID不存在: {invalid_ids}'}
            )

        exam = serializer.save(teacher=self.request.user)
        # 批量创建考试题目关联
        for q in questions_data:
            ExamQuestion.objects.create(
                exam=exam,
                question_id=q['question'],
                score=q['score']
            )
        # 处理指定学生
        student_ids = self.request.data.get('student_ids', [])
        if student_ids:
            exam.students.set(student_ids)

    def update(self, request, *args, **kwargs):
        exam = self.get_object()

        # 验证题目ID
        questions_data = request.data.get('exam_questions')
        if questions_data is not None:
            invalid_ids = self._validate_question_ids(questions_data)
            if invalid_ids:
                return Response(
                    {'exam_questions': f'以下题目ID不存在: {invalid_ids}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        response = super().update(request, *args, **kwargs)
        # 更新 exam_questions
        if questions_data is not None:
            exam.exam_questions.all().delete()
            for q in questions_data:
                ExamQuestion.objects.create(
                    exam=exam,
                    question_id=q['question'],
                    score=q['score']
                )
        # 更新指定学生
        student_ids = request.data.get('student_ids')
        if student_ids is not None:
            exam.students.set(student_ids)
        return response

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """学生开始考试（校验时间）"""
        exam = self.get_object()
        now = timezone.now()
        if now < exam.start_time:
            return Response({'error': '考试尚未开始'}, status=status.HTTP_400_BAD_REQUEST)
        if now > exam.end_time:
            return Response({'error': '考试已结束'}, status=status.HTTP_400_BAD_REQUEST)

        questions = [
            {
                'id': eq.question.id,
                'description': eq.question.description,
                'score': eq.score,
            }
            for eq in exam.exam_questions.all()
        ]
        return Response({
            'message': '开始考试',
            'exam_title': exam.title,
            'total_score': exam.total_score,
            'questions': questions,
        })

    @action(detail=True, methods=['get'])
    def result(self, request, pk=None):
        """查看考试结果与排名"""
        exam = self.get_object()
        from apps.submissions.models import Submission
        from django.db.models import Max, Sum

        # 按学生聚合最高总分排名
        ranking = (
            Submission.objects
            .filter(exam=exam)
            .values('student__id', 'student__username')
            .annotate(total=Sum('score'))
            .order_by('-total')
        )
        return Response({
            'exam_title': exam.title,
            'ranking': list(ranking),
        })
