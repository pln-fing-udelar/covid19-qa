import json
import requests


from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from management.models import QueryConf

from .models import Answer, Question
from .serializers import (AnswerSerializer, AnswerFeedbackInputSerializer, ParagraphFeedbackInputSerializer, FeedbackSerializer,
                          QuestionInputSerializer)


class QuestionApiView(APIView):

    @transaction.atomic
    def post(self, request):
        question_serializer = QuestionInputSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)
        question = question_serializer.validated_data['question'].lower()
        question_obj, _ = Question.objects.get_or_create(question=question)
        query_conf = None
        es_query_conf = QueryConf.objects.filter(parameter_name='ES_QUERY_CONF').first()
        if es_query_conf:
            query_conf = es_query_conf.conf

        qa_response = requests.post(
            f'{settings.QA_SERVER}/Covid19-QA/question',
            json={
                'question': question,
                'es_query_conf': json.dumps(query_conf),
                }
        )
        answers = qa_response.json()
        if qa_response.status_code != 200:
            return Response(answers, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

class ParagraphFeedbackApiView(APIView):
    @transaction.atomic
    def post(self, request):
        paragraph_feedback_serializer = ParagraphFeedbackInputSerializer(data=request.data)
        paragraph_feedback_serializer.is_valid(raise_exception=True)
        answer = get_object_or_404(
            Answer, id=paragraph_feedback_serializer.validated_data['answer_id']
        )
        answer.paragraph_feedback = paragraph_feedback_serializer.validated_data['paragraph_feedback']
        answer.save()
        return Response(status=204)

class AnswerFeedbackApiView(APIView):
    @transaction.atomic
    def post(self, request):
        answer_feedback_serializer = AnswerFeedbackInputSerializer(data=request.data)
        answer_feedback_serializer.is_valid(raise_exception=True)
        answer = get_object_or_404(
            Answer, id=answer_feedback_serializer.validated_data['answer_id']
        )
        answer.answer_feedback = answer_feedback_serializer.validated_data['answer_feedback']
        answer.save()
        return Response(status=204)


class AnswersApiView(APIView):
    queryset = Answer.objects

    def get(self, request):
        feedback_serializer = FeedbackSerializer(self.queryset.all(), many=True)
        return Response(feedback_serializer.data)


class ExactMatchApiView(AnswersApiView):
    queryset = Answer.objects.filter(answer_feedback=Answer.EXACT_MATCH)


class ContainedMatchApiView(AnswersApiView):
    queryset = Answer.objects.filter(answer_feedback=Answer.CONTAINED_MATCH)


class IncompleteMatchApiView(AnswersApiView):
    queryset = Answer.objects.filter(answer_feedback=Answer.INCOMPLETE_MATCH)


class NoMatchApiView(AnswersApiView):
    queryset = Answer.objects.filter(answer_feedback=Answer.NO_MATCH)
    

class UnrelatedParagraphsApiView(AnswersApiView):
    queryset = Answer.objects.filter(paragraph_feedback=Answer.UNRELATED_PARAGRAPHS)


class RelatedParagraphsApiView(AnswersApiView):
    queryset = Answer.objects.filter(paragraph_feedback=Answer.RELATED_PARAGRAPHS)


class GoodParagraphsApiView(AnswersApiView):
    queryset = Answer.objects.filter(paragraph_feedback=Answer.GOOD_PARAGRAPHS)


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
                "source": "La Diaria",
                "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/",
                "prob": 0.76,
                "logit": 6.24
            },
            {
                "title": "Información de interés actualizada sobre coronavirus COVID ",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 12,
                "answer_end_index": 85,
                "date": "03/04/2020",
                "source": "La Diaria",
                "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/",
                "prob": 0.15,
                "logit": 11.45
            },
            {
                "title": "Plan Nacional Coronavirus | Ministerio de Salud Pública",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 27,
                "answer_end_index": 96,
                "date": "18/04/2020",
                "source": "La Diaria",
                "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/",
                "prob": 0.10,
                "logit": 2.45
            },
            {
                "title": "Coronavirus en América: últimas noticias de la covid-19, en ...",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 50,
                "answer_end_index": 105,
                "date": "05/03/2020",
                "source": "La Diaria",
                "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/",
                "prob": 0.02,
                "logit": -0.0001
            },
            {
                "title": "Coronavirus (CoV) GLOBAL - World Health Organization",
                "context": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto voluptas in itaque, "
                           "debitis voluptatibus ab illum doloribus nemo sed vero optio veritatis repellat minima "
                           "quae ex quo asperiores reiciendis reprehenderit.",
                "answer_start_index": 4,
                "answer_end_index": 96,
                "date": "20/02/2020",
                "source": "La Diaria",
                "url": "https://ladiaria.com.uy/articulo/2020/4/hasta-este-sabado-habia-517-casos-de-coronavirus/",
                "prob": 0.00001,
                "logit": -10.231
            }
        ]
        return Response(hardcoded_response)
