from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import *
from .models import Preferences, ParkingPlace, ParkingPlaceType, ParkingPlaceStatus, Log
from django.contrib.auth.decorators import login_required
from django.views import View
from datetime import datetime as dt
from django.conf import settings
from django.contrib.auth.models import User



class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is None:
                return redirect(reverse("login"))

            if not user.is_active:
                return redirect(reverse("login"))

            login(request, user)
            return redirect(reverse("index"))

        return render(request, "registration/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            Preferences.objects.create(user=new_user)

            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'],
                                    )
            login(request, new_user)

            return redirect(reverse("personal_area"))

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, "registration/reg_setting.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
def account(request):

    preferences_form = PreferencesForm(instance=request.user.preferences)
    question_form = QuestionForm()

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect(reverse("personal_area"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(
        request,
        'main/personal_area.html',
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "preferences_form": preferences_form,
            "question_form": question_form,
        }
    )


def update_preferences(request):
    if request.method == "POST":
        preferences_form = PreferencesForm(instance=request.user.preferences, data=request.POST)
        if preferences_form.is_valid():
            preferences_form.save()
            return redirect(reverse("personal_area"))

    return redirect(reverse("personal_area"))


@login_required
def index(request):

    data = request.GET
    places = None
    if data:
        # places = {i: "booked" if randint(0, 1) else "" for i in range(1, 26)}
        places = ParkingPlace.objects.all().filter(parking__pk=data['address'])
        preferences = request.user.preferences
        place_types = None

        if any([data["is_open"], data["location"], data.get("is_for_disabled")]):
            place_types = ParkingPlaceType.objects.all()
            if data["is_open"]:
                place_types = place_types.filter(is_open=data["is_open"])
            if data["location"]:
                place_types = place_types.filter(location=data["location"])
            if data.get("is_for_disabled"):
                place_types = place_types.filter(is_for_disabled=True)
        elif preferences.is_exist():
            place_types = ParkingPlaceType.objects.all()
            print(preferences.is_open)
            if not(isinstance(preferences.is_open, type(None))):
                place_types = place_types.filter(is_open=preferences.is_open)
            if not(isinstance(preferences.location, type(None))):
                place_types = place_types.filter(location=preferences.location)
            if preferences.is_for_disabled:
                place_types = place_types.filter(is_for_disabled=True)

        if place_types:
            places = places.filter(place_type__in=place_types)

        place_status = None
        if data.get("free"):
            place_status = ParkingPlaceStatus.objects.get(status="Свободно")
        elif data.get("occupied"):
            place_status = ParkingPlaceStatus.objects.get(status="Занято")

        if place_status:
            places = places.filter(status=place_status)

        type_form = ParkingPlaceTypeForm(data=data)
        parking_form = ParkingForm(data=data)
    else:
        type_form = ParkingPlaceTypeForm()
        parking_form = ParkingForm()

    return render(
        request,
        "main/index.html",
        {
            "places": places,
            "type_form": type_form,
            "parking_form": parking_form,
        }
    )


def booking(request, uid):

    profile = request.user.profile
    if profile.is_user_booking():
        return redirect(reverse("index"))

    try:
        parking_place = ParkingPlace.objects.get(id=uid)

        parking_place.status = ParkingPlaceStatus.objects.get(status="Занято")
        profile.booked_place = parking_place
        profile.save()
        parking_place.save()

        Log.objects.create(user=request.user, parking_place=parking_place, date=dt.now())

        messages.success(request, "Вы успешно забронировали место. Информацию можно посмотреть в личном кабинете")
    except Exception as e:
        messages.info(request, "Что-то пошло не так")

    return redirect(reverse("index"))


def stop_booking(request, uid):

    profile = request.user.profile
    if profile.id != uid:
        return redirect(reverse("personal_area"))

    try:
        parking_place = profile.booked_place
        parking_place.status = ParkingPlaceStatus.objects.get(status="Свободно")
        profile.booked_place = None
        profile.save()
        parking_place.save()
    except Exception as e:
        print(e)

    Log.objects.create(user=request.user, parking_place=parking_place, date=dt.now(), status=False)
    return redirect(reverse("personal_area"))


def question(request):

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.save()
            new_question.link = f"http://localhost:8000/question/response/{new_question.id}/"
            new_question.save()

    return redirect(reverse("personal_area"))


def question_response(request, uid):

    if not request.user.is_superuser:
        return redirect(reverse("index"))

    user_question = Question.objects.all().filter(id=uid).first()
    if not user_question:
        return redirect("/admin")

    if request.method == "POST":
        response = request.POST['question-response']
        send_mail("Задачи", response, settings.EMAIL_HOST_USER, [user_question.user.email])
        user_question.status = 1
        user_question.save()
        return redirect("/admin")

    return render(
        request,
        "main/question_response.html",
        {
            "question": user_question
        }
    )


def remove(request, uid):

    if request.user.id == uid:
        User.objects.get(id=uid).delete()

    return redirect(reverse('index'))


