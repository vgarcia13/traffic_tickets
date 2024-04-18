from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class CreatePersonsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=50, allow_blank=False, allow_null=False)
    full_name = serializers.CharField(required=True, max_length=200, allow_blank=False, allow_null=False)

    class Meta:
        model = Person
        exclude = ('user',)


class PersonsSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('id', 'email', 'full_name', 'token')

    @staticmethod
    def get_token(obj):
        token = Token.objects.get(user=obj.user)
        return token.key


class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'plate', 'brand', 'model', 'color', 'year', 'owner')


class GetVehiclesSerializer(serializers.ModelSerializer):
    owner = PersonsSerializer()

    class Meta:
        model = Vehicle
        fields = ('id', 'plate', 'brand', 'model', 'color', 'year', 'owner')


class GetOfficersSerializer(serializers.ModelSerializer):
    person = PersonsSerializer()

    class Meta:
        model = Officer
        fields = ('id', 'person')


class OfficersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = ('id', 'person')


class GetTicketsSerializer(serializers.ModelSerializer):
    vehicle = GetVehiclesSerializer()
    reporting_officer = GetOfficersSerializer()

    class Meta:
        model = Ticket
        fields = ('id', 'timestamp', 'notes', 'vehicle', 'reporting_officer')


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'timestamp', 'notes', 'vehicle', 'reporting_officer')


class CreateTicketsSerializer(serializers.ModelSerializer):
    plate = serializers.CharField()
    notes = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Ticket
        exclude = ('vehicle', 'reporting_officer')


class GenerateInformsSerializer(serializers.Serializer):
    email = serializers.CharField()
