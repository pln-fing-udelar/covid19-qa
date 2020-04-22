import requests

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Answer, Question

class QuestionApiView(APIView):

    def post(self, request):
        question = request.data.get('question')
        qa_response = requests.post(
            f'{settings.QA_SERVER}/Covid19-QA/question',
            json={'question': question}
        )
        question_obj = Question.objects.create(question=question)
        response = []
        for answer in qa_response.json():
            answer_obj = Answer.objects.create(
                question=question_obj,
                title=answer['title'],
                context=answer['context'],
                answer=answer['answer'],
            )
            answer['id'] = answer_obj.id
            response.append(answer)
        return Response(response)


class AnswerFeedbackApiView(APIView):
    
    def post(self, request):
        feedback = request.data.get('feedback')
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.get(id=answer_id)
        answer.feedback = feedback
        answer.save()
        return Response(status=200)