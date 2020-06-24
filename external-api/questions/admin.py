from django.contrib import admin
from .models import Answer, Question


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'feedback' , 'prob')
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)