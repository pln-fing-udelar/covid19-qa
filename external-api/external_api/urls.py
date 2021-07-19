from django.conf.urls import url
from django.contrib import admin

from management.views import ESQueryConfAPIView
from questions.views import (AnswerFeedbackApiView, ParagraphFeedbackApiView, FrequentQuestionsApiView, QuestionApiView,
                            ExactMatchApiView, ContainedMatchApiView, IncompleteMatchApiView, NoMatchApiView,
                            UnrelatedParagraphsApiView, RelatedParagraphsApiView, GoodParagraphsApiView)

urlpatterns = [
    url('admin/', admin.site.urls),
    url('question/', QuestionApiView.as_view()),
    url('answerFeedback/', AnswerFeedbackApiView.as_view()),
    url('paragraphFeedback/', ParagraphFeedbackApiView.as_view()),
    url('frequent-questions/', FrequentQuestionsApiView.as_view()),
    url('correct-answers/', ExactMatchApiView.as_view()),
    url('contained-answers/', ContainedMatchApiView.as_view()),
    url('incomplete-answers/', IncompleteMatchApiView.as_view()),
    url('wrong-answers/', NoMatchApiView.as_view()),
    url('unrelated-paragraphs/', UnrelatedParagraphsApiView.as_view()),
    url('related-paragraphs/', RelatedParagraphsApiView.as_view()),
    url('good-paragraphs/', GoodParagraphsApiView.as_view()),
    url('es-query-conf/', ESQueryConfAPIView.as_view()),
]
