from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import ParkingPlace
from main.api.serializers import *


class ParkingPlaceViewset(viewsets.ModelViewSet):
    queryset = ParkingPlace.objects.all()
    serializer_class = ParkingPlaceSerializer


class ParkingPlaceListView(generics.ListAPIView):
    queryset = ParkingPlace.objects.all()
    serializer_class = ParkingPlaceSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk", None)

        if not pk:
            return ParkingPlace.objects.all()

        return ParkingPlace.objects.filter(parking__pk=pk)


class ParkingPlaceStatusViewset(viewsets.ModelViewSet):
    queryset = ParkingPlaceStatus.objects.all()
    serializer_class = ParkingPlaceStatusSerializer


class ParkingViewset(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer


class ParkingPlaceTypeViewset(viewsets.ModelViewSet):
    queryset = ParkingPlaceType.objects.all()
    serializer_class = ParkingPlaceTypeSerializer


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class PreferencesViewset(viewsets.ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer


class LogViewset(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    def list(self, request):
        return Response({"logs":[log.__str__() for log in Log.objects.all()]})


