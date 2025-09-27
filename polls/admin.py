from django.contrib import admin
from .models import Poll, Choice, Vote

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id','title','created_by','created_at','is_active','expires_at')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id','text','poll')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id','poll','choice','user','voted_at')
