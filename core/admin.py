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
    
@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ["host"]
    filter_horizontal = ["players"]
    list_display = ["host", "created_time"]
    list_filter = ["host","is_active"]
    
@admin.register(models.UserResult)
class UserResultAdmin(admin.ModelAdmin):
    search_fields = ["user"]
    list_display = ["user", "score"]
    list_filter = ["game"]