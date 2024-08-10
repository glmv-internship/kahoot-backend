from django.contrib import admin

from core import models


class PollOptionInline(admin.StackedInline):
    exclude = ['created_time', 'last_updated_time']
    model = models.PollOption
    extra = 4


@admin.register(models.Poll)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [PollOptionInline]
    
class QuestionAdminInline(admin.StackedInline):
    model = models.Poll
    extra = 1

@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAdminInline]
    search_fields = ["name"]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["uid", "full_name"]