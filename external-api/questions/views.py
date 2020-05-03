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
        if qa_response.status_code == 400:
            return qa_response
        question_obj = Question.objects.create(question=question)
        response = []
        for answer in qa_response.json():
            print(answer)
            answer_obj = Answer.objects.create(
                question=question_obj,
                title=answer['title'],
                context=answer['context'],
                answer=answer['answer'],
            )
            answer['id'] = answer_obj.id
            response.append(answer)
        return Response(qa_response.json())


class AnswerFeedbackApiView(APIView):
    def post(self, request):
        feedback = request.data.get('feedback')
        answer_id = request.data.get('answer_id')
        answer = Answer.objects.get(id=answer_id)
        answer.feedback = feedback
        answer.save()
        return Response(status=204)


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
