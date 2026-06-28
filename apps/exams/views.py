from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Exam, ExamQuestion
from .serializers import ExamSerializer, ExamQuestionSerializer
from apps.users.permissions import IsTeacher


class ExamViewSet(viewsets.ModelViewSet):
    """考试管理 ViewSet"""
    serializer_class = ExamSerializer

    def get_queryset(self):
        user = self.request.user
        base_qs = Exam.objects.all().prefetch_related('exam_questions__question')
        if user.user_type == 'teacher':
            # 教师只看自己创建的考试
            return base_qs.filter(teacher=user)
        # 学生可以看到所有考试
        return base_qs

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        exam = serializer.save(teacher=self.request.user)
        # 批量创建考试题目关联
        questions_data = self.request.data.get('exam_questions', [])
        for q in questions_data:
            ExamQuestion.objects.create(
                exam=exam,
                question_id=q['question'],
                score=q['score']
            )

    def update(self, request, *args, **kwargs):
        exam = self.get_object()
        response = super().update(request, *args, **kwargs)
        # 更新 exam_questions
        questions_data = request.data.get('exam_questions')
        if questions_data is not None:
            exam.exam_questions.all().delete()
            for q in questions_data:
                ExamQuestion.objects.create(
                    exam=exam,
                    question_id=q['question'],
                    score=q['score']
                )
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
