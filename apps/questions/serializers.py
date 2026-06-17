from rest_framework import serializers
from .models import Question, Answer, TestCase


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'correct_sql')


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ('id', 'test_input', 'expected_output')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('teacher', 'created_at')


class QuestionStudentSerializer(serializers.ModelSerializer):
    """学生视角：不暴露正确答案和建表语句"""
    test_cases = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id', 'title', 'description', 'difficulty', 'sample_input',
            'sample_output', 'teacher', 'created_at',
            'test_cases',
        )
        read_only_fields = ('teacher', 'created_at')
