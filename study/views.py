# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import ModelForm, UserForm, MyUserCreationForm
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.permissions import IsAuthenticated


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not correct')
    return render(request, 'study/login-register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured')
    return render(request, 'study/login-register.html', {'form': form})


def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=query) | Q(
        name__icontains=query) | Q(description__icontains=query))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=query))
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, "room_messages": room_messages}
    return render(request, 'study/home.html', context)


def room(request, slug):
    room = Room.onjects.get(id=slug)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', slug=room.id)
    constext = {'room': room, 'messages': room_messages,
                'participants': participants}
    return render(request, 'study/room.html', context)


@login_required(login_url='login')
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'study/room-form.html', context)


@login_required(login_url='login')
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def updateRoom(request, slug):
    room = Room.objects.get(id=slug)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'study/room-form.html', context)


@login_required(login_url='login')
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def deleteRoom(request, slug):
    room = Room.objects.get(id=slug)

    if request.user != room.host:
        return HttpResponse('You are not allowed!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'study/delete.html', {'obj': room})


@login_required(login_url='login')
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def deleteComment(request, slug):
    message = Message.objects.get(id=slug)

    if request.user != message.user:
        return HttpResponse('You are not allowed!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'study/delete.html', {'obj': message})


def userProfile(request, slug):
    user = User.objects.get(id=slug)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topics.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_message': room_message, 'topics': topics}
    return render(request, 'study/profile.html', context)


@login_required(login_url='login')
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', slug=user.id)
    return render(request, 'study/update-user.html', {'form': form})


def topicsPage(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=query)
    return render(request, 'study/topics.html', {'topics': topics})


def activitiesPage(request):
    room_messages = Message.objects.all()
    return render(request, 'study/activities.html', {'room_messages': room_messages})


# class CustomTokenObtainPairView(TokenObtainPairView):
#     # Customize payload data if needed
#     pass
