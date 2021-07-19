from rest_framework import serializers

from .models import Answer


class QuestionInputSerializer(serializers.Serializer):
    question = serializers.CharField()


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    context = serializers.CharField()
    answer = serializers.CharField()
    answer_start_index = serializers.CharField()
    answer_end_index = serializers.CharField()
    date = serializers.CharField()
    source = serializers.CharField()
    url = serializers.CharField()
    prob = serializers.CharField()
    logit = serializers.CharField()


class AnswerFeedbackInputSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()
    answer_feedback = serializers.ChoiceField(choices=Answer.ANSWER_FEEDBACK_CHOICES)

class ParagraphFeedbackInputSerializer(serializers.Serializer):
    answer_id = serializers.IntegerField()
    paragraph_feedback = serializers.ChoiceField(choices=Answer.PARAGRAPH_FEEDBACK_CHOICES)

class FeedbackSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(source='question.question')
    context = serializers.CharField()
    answer = serializers.CharField()
    answer_date = serializers.DateTimeField(source='created_at')
