from django.db import models
from django.contrib.auth.models import User
from .choices import *


class Parking(models.Model):

    address = models.CharField("Адрес", max_length=255)

    def __str__(self):
        return f"{self.address}"

    class Meta:
        verbose_name_plural = "Парковки"


class ParkingPlaceType(models.Model):

    is_open = models.IntegerField("Открытое-закрытое", choices=OPEN_CHOICE, null=True, blank=True)
    location = models.IntegerField("Расположение", choices=LOCATION_CHOICE, null=True, blank=True)
    is_for_disabled = models.BooleanField("Место для инвалидов", default=False)

    def __str__(self):
        response = f"{self.get_is_open_display()} "
        response += f"{self.get_location_display() or ''}"
        response += f"{'Для инвалидов' if self.is_for_disabled else ''}"
        return response

    class Meta:
        verbose_name_plural = "Типы парковочных мест"


class ParkingPlaceStatus(models.Model):

    status = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name_plural = "Статусы парковочных мест"


def get_last_number():
    if ParkingPlace.objects.last():
        return ParkingPlace.objects.last().number + 1
    return 1


class ParkingPlace(models.Model):

    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name="places")
    number = models.IntegerField(default=get_last_number)
    status = models.ForeignKey(ParkingPlaceStatus, on_delete=models.SET_NULL, null=True, related_name="places")
    place_type = models.ForeignKey(ParkingPlaceType, on_delete=models.SET_NULL, null=True, related_name="places")

    def __str__(self):
        return f"{self.number} - {self.parking.address}"

    def is_booked(self):
        if self.status.status == "Занято":
            return True
        return False

    def get_info(self):
        response = f"{self.place_type.get_is_open_display() or ''}<br>"
        response += f"{self.place_type.get_location_display() or ''}<br>"
        response += f"{'Для инвалидов' if self.place_type.is_for_disabled else ''}"
        return response

    class Meta:
        verbose_name_plural = "Парковочные места"


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_number = models.CharField("Номер машины", max_length=8)
    birthdate = models.DateField("Дата рождения", blank=True, null=True)
    is_booking = models.BooleanField("Бронирует", default=False)
    booked_place = models.ForeignKey(ParkingPlace, related_name="profile", on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.car_number}"

    def is_user_booking(self):
        if self.booked_place:
            return True
        return False

    class Meta:
        verbose_name_plural = "Профили"


class Question(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField("Вопрос", max_length=500)
    status = models.IntegerField("Статус", choices=STATUS_CHOICES, default=0)
    link = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: {self.get_status_display()}"

    class Meta:
        verbose_name_plural = "Вопросы"


class Preferences(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_any = models.BooleanField("Любое", default=True)
    is_open = models.IntegerField("Открытое-закрытое", choices=OPEN_CHOICE, null=True, blank=True)
    location = models.IntegerField("Расположение", choices=LOCATION_CHOICE, null=True, blank=True)
    is_for_disabled = models.BooleanField("Место для инвалидов", default=False)

    def __str__(self):
        if self.is_any:
            return "Любое"
        response = f"{self.get_is_open_display()} - "
        response += f"{self.get_location_display() or 'Не указано'} - "
        response += f"{'Для инвалидов' if self.is_for_disabled else ''}"
        return response

    def is_exist(self):
        return any([not(self.is_open is None), not(self.location is None), self.is_for_disabled])

    def save(self, *args, **kwargs):
        if self.is_any and self.is_exist():
            self.is_open = None
            self.location = None
            self.is_for_disabled = False
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Предпочтение пользователей"


class Log(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    parking_place = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE, related_name="logs")
    date = models.DateTimeField()
    status = models.BooleanField(default=True)

    def __str__(self):
        if self.status:
            return f"{self.date.strftime('%d/%m/%y %H:%M:%S')}:{self.user.first_name} {self.user.last_name} забронирова {self.parking_place.number}е " \
                f"парковочное место на {self.parking_place.parking.address}"
        return f"{self.date.strftime('%d/%m/%y %H:%M:%S')}:{self.user.first_name} {self.user.last_name} бронь завершена {self.parking_place.number}е " \
                f"парковочное место на {self.parking_place.parking.address}"

    class Meta:
        verbose_name_plural = "Логи"
