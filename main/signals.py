from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ParkingPlace


@receiver(post_delete, sender=ParkingPlace, dispatch_uid='place_delete_signal')
def delete_parking_place(sender, instance, **kwargs):
    parking = instance.parking
    for place in ParkingPlace.objects.all().filter(parking=parking).filter(number__gte=instance.number):
        place.number -= 1
        place.save()
