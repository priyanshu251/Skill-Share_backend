from django.db import models

# Create your models here.

class Chat(models.Model):
    CHAT_TYPES = (
        ('dm', 'Direct Message'),
        ('gc', 'Group Chat'),
    )
    type = models.CharField(max_length=2, choices=CHAT_TYPES)
    name = models.CharField(max_length=255,default="")
    participants = models.ManyToManyField("user.User", related_name='chats')
    last_message_time = models.DateTimeField(auto_now=True)
    document_id = models.CharField(max_length=256,primary_key=True)