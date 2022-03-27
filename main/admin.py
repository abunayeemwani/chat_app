from django.contrib import admin
from .models import Thread, Message, Member

admin.site.register(Message)

class Message(admin.TabularInline):
    model = Message

class ThreadAdmin(admin.ModelAdmin):
    inlines = [Message]
    class Meta:
        model = Thread

class MemberAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Member, MemberAdmin)