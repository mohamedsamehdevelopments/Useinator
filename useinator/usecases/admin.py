from django.contrib import admin
from .models import Category, Question, Result, Answer, Project

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Answer)
admin.site.register(Project)