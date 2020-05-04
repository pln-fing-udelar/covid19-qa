import requests

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Answer, Question
from .serializers import (AnswerSerializer, FeedbackInputSerializer, FeedbackSerializer,
                          QuestionInputSerializer)


class QuestionApiView(APIView):
    
    @transaction.atomic
    def post(self, request):
        question_serializer = QuestionInputSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)
        question = question_serializer.validated_data['question'].lower()
        question_obj, _ = Question.objects.get_or_create(question=question)
        qa_response = requests.post(
            f'{settings.QA_SERVER}/Covid19-QA/question',
            json={'question': question}
        )
        answers = qa_response.json()
        if qa_response.status_code != 200:
            return qa_response
        for answer in answers:
            answer_obj = Answer.objects.create(
                question=question_obj,
                title=answer['title'],
                context=answer['context'],
                answer=answer['answer'],
            )
            answer['id'] = answer_obj.id
        answer_serializer = AnswerSerializer(data=answers, many=True)
        answer_serializer.is_valid(raise_exception=True)
        return Response(answer_serializer.validated_data)


class AnswerFeedbackApiView(APIView):
    @transaction.atomic
    def post(self, request):
        feedback_serializer = FeedbackInputSerializer(data=request.data)
        feedback_serializer.is_valid(raise_exception=True)
        answer = get_object_or_404(
            Answer, id=feedback_serializer.validated_data['answer_id']
        )
        answer.feedback = feedback_serializer.validated_data['feedback']
        answer.save()
        return Response(status=204)



class AnswersApiView(APIView):
    
    queryset = Answer.objects
    def get(self, request):
        feedback_serializer = FeedbackSerializer(self.queryset.all(), many=True)
        return Response(feedback_serializer.data)


class CorrectApiView(AnswersApiView):
    queryset = Answer.objects.filter(feedback=Answer.CORRECT)


class WrongApiView(AnswersApiView):
    queryset = Answer.objects.filter(feedback=Answer.WRONG)


class FakeApiView(AnswersApiView):
    queryset = Answer.objects.filter(feedback=Answer.FAKE)


class FrequentQuestionsApiView(APIView):
    def get(self, request):
        hardcoded_response = [
            {
                "title": "Murió la décima persona por coronavirus en ... - Montevideo",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 6,
                "answer_end_index": 36,
                "date": "25/03/2020",
                "source": {
                    "name": "La Diaria",
                    "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/"
                }
            },
            {
                "title": "Información de interés actualizada sobre coronavirus COVID ",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 12,
                "answer_end_index": 85,
                "date": "03/04/2020",
                "source": {
                    "name": "La Diaria",
                    "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/"
                }
            },
            {
                "title": "Plan Nacional Coronavirus | Ministerio de Salud Pública",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 27,
                "answer_end_index": 96,
                "date": "18/04/2020",
                "source": {
                    "name": "La Diaria",
                    "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/"
                }
            },
            {
                "title": "Coronavirus en América: últimas noticias de la covid-19, en ...",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 50,
                "answer_end_index": 105,
                "date": "05/03/2020",
                "source": {
                    "name": "La Diaria",
                    "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/"
                }
            },
            {
                "title": "Coronavirus (CoV) GLOBAL - World Health Organization",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 4,
                "answer_end_index": 96,
                "date": "20/02/2020",
                "source": {
                    "name": "La Diaria",
                    "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/"
                }
            }
        ]
        return Response(hardcoded_response)
