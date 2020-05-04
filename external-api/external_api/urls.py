from django.conf.urls import include, url
from django.contrib import admin

from questions.views import (AnswerFeedbackApiView, CorrectApiView, QuestionApiView,
                             FrequentQuestionsApiView, WrongApiView, FakeApiView)

urlpatterns = [
    url('admin/', admin.site.urls),
    url('question/', QuestionApiView.as_view()),
    url('feedback/', AnswerFeedbackApiView.as_view()),
    url('frequent-questions/', FrequentQuestionsApiView.as_view()),
    url('correct-answers/', CorrectApiView.as_view()),
    url('wrong-answers/', WrongApiView.as_view()),
    url('fake-answers/', FakeApiView.as_view()),
]
