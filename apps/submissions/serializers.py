from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)
    question_desc = serializers.CharField(source='question.description', read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = (
            'student', 'submission_time', 'execution_status', 'score'
        )
