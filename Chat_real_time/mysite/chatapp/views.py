from django.shortcuts import render
from .models import ChatRoom, ChatMessage

# Create your views here.

def index(req):
    chatrooms = ChatRoom.objects.all()
    return render(req, 'index.html', {'chatrooms':chatrooms})

def chatroom(req, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    messages = ChatMessage.objects.filter(room=chatroom)[0:31]
    return render(req, 'room.html', {'chatroom':chatroom, 'messages':messages})