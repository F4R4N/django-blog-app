from django.contrib import admin
from .models import Post, Comment, Subscriber, Newsletter
from django.core.mail import send_mail
import os

my_email = os.environ.get('PTSEENV')


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status',)
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Subscriber)
class SubscriberShow(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'active')


def send_newsletter(self, request, queryset):
    subscribers = Subscriber.objects.all().filter(active=True)
    data = queryset
    subject = ""
    message = ""
    for i in queryset:
        subject = i.subject
    for j in queryset:
        message = j.body
        
    for user in subscribers:
        body = "Hello, " + user.name + "\n\n" + message + "\n\n\n" + "" # TODO : add unsubscribe the newsletter
        email = user.email
        send_mail(subject, body, my_email, [email])

    send_newsletter.short_description = "send email"


@admin.register(Newsletter)
class NewNewsletter(admin.ModelAdmin):
    list_display = ('subject', 'body')
    actions = [send_newsletter]

    












