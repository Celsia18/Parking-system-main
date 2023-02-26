from rest_framework import serializers
from main.models import *


class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = ['id', 'address']


class ParkingPlaceStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingPlaceStatus
        fields = ['status']


class ParkingPlaceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingPlaceType
        fields = ['is_open', 'location', 'is_for_disabled']


class ParkingPlaceSerializer(serializers.ModelSerializer):
    # parking = ParkingSerializer(many=False, read_only=True)
    # status = ParkingPlaceStatusSerializer(many=False, read_only=True)
    # place_type = ParkingPlaceTypeSerializer(many=False, read_only=True)

    class Meta:
        model = ParkingPlace
        fields = ['id', 'parking', 'number', 'status', 'place_type']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Question
        fields = "__all__"
        # read_only_fields = ("user", )


class PreferencesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preferences
        fields = "__all__"
        # read_only_fields = ("user", )


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = "__all__"
        # read_only_fields = ("user", )