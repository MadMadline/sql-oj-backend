from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsTeacher, IsOwnerOrTeacher
from apps.submissions.models import Submission
from apps.questions.models import Question
from apps.exams.models import Exam


class RegisterView(generics.CreateAPIView):
    """用户注册 — 公开接口"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    """用户管理 ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsTeacher()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """教师可以看到所有学生（方便分配考试等），学生只能看自己"""
        qs = super().get_queryset()
        if self.request.user.user_type == 'teacher':
            return qs.filter(user_type='student') | User.objects.filter(id=self.request.user.id)
        if self.request.user.user_type == 'student':
            return qs.filter(id=self.request.user.id)
        return qs

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """查看或修改当前登录用户信息"""
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me/stats')
    def my_stats(self, request):
        """当前用户的个人统计数据"""
        user = request.user

        if user.user_type == 'teacher':
            # 教师：统计自己创建的题目和考试数量
            return Response({
                'username': user.username,
                'user_type': 'teacher',
                'questions_created': Question.objects.filter(teacher=user).count(),
                'exams_created': Exam.objects.filter(teacher=user).count(),
            })

        # 学生：统计提交和通过率
        submissions = Submission.objects.filter(student=user)
        total = submissions.count()
        passed = submissions.filter(execution_status='ACCEPTED').count()

        recent = submissions.order_by('-submission_time')[:5].values(
            'id', 'question__id', 'question__title',
            'execution_status', 'score', 'submission_time'
        )

        return Response({
            'username': user.username,
            'user_type': user.user_type,
            'total_submissions': total,
            'passed': passed,
            'pass_rate': round(passed / total, 2) if total else 0,
            'recent_submissions': list(recent),
        })
