from django.db import models
from django.conf import settings


class Exam(models.Model):
    STUDENT_SCOPE_CHOICES = [
        ('all', '所有学生'),
        ('specified', '指定学生'),
    ]
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_score = models.IntegerField()
    student_scope = models.CharField(
        max_length=10, choices=STUDENT_SCOPE_CHOICES, default='all'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_exams',
        limit_choices_to={'user_type': 'student'}
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name='exams'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exam'


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_questions')
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        db_table = 'exam_question'
        unique_together = ('exam', 'question')
