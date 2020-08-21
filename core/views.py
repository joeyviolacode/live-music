from django.shortcuts import render, redirect, get_object_or_404
from .models import Musician, MusicianComment, Event, EventComment
from .forms import MusicianForm, EventForm, DonationForm
from users.models import User
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import json
import datetime
import os

# Create your views here.
class Homepage(View):
    def get(self, request):
        events = Event.objects.all()
        return render(request, 'core/homepage.html', {'events': events})


class EventPage(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        # Passing data through to react via json. MUST USE DOUBLE QUOTES
        return render(request, 'core/event.html', {
            'data': json.dumps({
                "pk": pk,
                "ownerId": event.owner.user.id,
                "userId": request.user.id,
                "port": os.getenv('PORT') if os.getenv('PORT') else 3000
            }), 
            "event": event,
        })


class AddEvent(View):
    def get(self, request, musician_pk):
        musician = get_object_or_404(Musician, pk=musician_pk)
        if musician.user == request.user:
            form = EventForm()
            return render(request, 'core/create_event.html', {"form": form, "musician": musician})
        return redirect(to="show-musician", musician_pk=musician_pk)

    def post(self, request, musician_pk):
        musician = get_object_or_404(Musician, pk=musician_pk)
        if musician.user == request.user:
            form = EventForm(data=request.POST, files=request.FILES)
            print(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.owner = musician
                event.save()
                return redirect(to="event", pk=event.pk)
            return redirect(to="show-musician", musician_pk=musician_pk)
        return redirect(to="show-musician", musician_pk=musician_pk)


class AddMusicianInfo(View):
    def get(self, request, user_pk):
        if get_object_or_404(User, pk=user_pk) == request.user:
            form = MusicianForm()
            return render(request, 'core/musician_form.html', {"form": form})
        return redirect(to="homepage")

    def post(self, request, user_pk):
        if get_object_or_404(User, pk=user_pk) == request.user:
            form = MusicianForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                musician = form.save(commit=False)
                musician.user = request.user
                musician.save()
                return redirect(to='show-musician', musician_pk=musician.pk)
            return redirect(to="homepage")
        return redirect(to="homepage")


class ShowMusician(View):
    def get(self, request, musician_pk):
        musician = get_object_or_404(Musician, pk=musician_pk)
        return render(request, 'core/show_musician.html', {"musician": musician})


class AddDonationInfo(View):
    def get(self, request, musician_pk):
        print("post attempt")        
        musician = get_object_or_404(Musician, pk=musician_pk)
        if musician.user == request.user:
            form = DonationForm(instance=musician)
            return render(request, 'core/donation_form.html', {"form": form , "musician": musician})
        return redirect(to="homepage")

    def post(self, request, musician_pk):
        musician = get_object_or_404(Musician, pk=musician_pk)
        print("post attempt")
        # if musician.user == request.user:
        form = DonationForm(instance=musician, data=request.POST, files=request.FILES)
        if form.is_valid():
            musician = form.save(commit=False)
            musician.user = request.user
            musician.save()
            return redirect(to='show-musician', musician_pk=musician_pk)
            # return redirect(to="homepage")
        return redirect(to="homepage")


def edit_event(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    musician = event.owner
    if request.method == "POST":
        form = EventForm(instance=event, data=request.POST, files=request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = musician
            event = form.save()
            return redirect(to="event", pk=event_pk)
    else:
        form = EventForm(instance=event)

    return render(
        request,
        "core/edit_event.html",
        {"form": form, "event": event, "musician": musician}  
    )

@method_decorator(csrf_exempt, name="dispatch")
class FavoriteMusician(View):
    def post(self, request, musician_pk):
        musician = get_object_or_404(Musician, pk=musician_pk)
        user = request.user
        if musician in user.favorite_musician.all():
            user.favorite_musician.remove(musician)
            return JsonResponse({"favorite": False})

        else:
            user.favorite_musician.add(musician)
            return JsonResponse({"favorite": True})




