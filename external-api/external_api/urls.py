from django.conf.urls import url
from django.contrib import admin

from management.views import ESQueryConfAPIView
from questions.views import (AnswerFeedbackApiView, CorrectApiView, QuestionApiView,
                             FrequentQuestionsApiView, WrongApiView, FakeApiView,
                             PartialApiView)

urlpatterns = [
    url('admin/', admin.site.urls),
    url('question/', QuestionApiView.as_view()),
    url('feedback/', AnswerFeedbackApiView.as_view()),
    url('frequent-questions/', FrequentQuestionsApiView.as_view()),
    url('partial-correct-answers/', PartialApiView.as_view()),
    url('correct-answers/', CorrectApiView.as_view()),
    url('wrong-answers/', WrongApiView.as_view()),
    url('fake-answers/', FakeApiView.as_view()),
    url('es-query-conf/', ESQueryConfAPIView.as_view()),
]