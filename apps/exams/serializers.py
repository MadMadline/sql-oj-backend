from rest_framework import serializers
from .models import Exam, ExamQuestion
from apps.users.models import User


class ExamQuestionSerializer(serializers.ModelSerializer):
    question_title = serializers.CharField(source='question.title', read_only=True)
    question_id = serializers.IntegerField(source='question.id', read_only=True)

    class Meta:
        model = ExamQuestion
        fields = ('id', 'question', 'question_id', 'question_title', 'score')


class ExamSerializer(serializers.ModelSerializer):
    exam_questions = ExamQuestionSerializer(many=True, read_only=True)
    student_ids = serializers.PrimaryKeyRelatedField(
        source='students', many=True, queryset=User.objects.filter(user_type='student'),
        required=False, write_only=True
    )

    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ('teacher', 'created_at', 'students')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['students'] = list(instance.students.values('id', 'username'))
        return data
