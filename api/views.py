from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import *
from .models import *


class PersonsViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = CreatePersonsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Person.objects.all()
        serializer = PersonsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Person.objects.all()
        try:
            person = get_object_or_404(queryset, pk=pk)
        except ValidationError:
            raise NotFound("Person not found")
        else:
            serializer = PersonsSerializer(person)
            return Response(serializer.data)

    def create(self, request):
        serializer = CreatePersonsSerializer(data=request.data)
        if serializer.is_valid():
            person = Person.objects.filter(
                email=serializer.validated_data['email']
            )

            if person:
                response_serializer = PersonsSerializer(person)
                return Response(response_serializer.data, status=200)

            user, is_new = User.objects.get_or_create(username=serializer.validated_data['email'])
            if is_new:
                user.save()

            token, is_new = Token.objects.get_or_create(user=user)
            if is_new:
                token.save()

            person = Person.objects.create(
                user=user,
                full_name=serializer.validated_data['full_name'],
                email=serializer.validated_data['email']
            )

            person.save()

            response_serializer = PersonsSerializer(person)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class VehiclesViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehiclesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Vehicle.objects.all()
        serializer = GetVehiclesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Vehicle.objects.all()
        try:
            vehicle = get_object_or_404(queryset, pk=pk)
        except ValidationError:
            raise NotFound("Vehicle not found")
        else:
            serializer = GetVehiclesSerializer(vehicle)
            return Response(serializer.data)

    def create(self, request):
        serializer = VehiclesSerializer(data=request.data)
        if serializer.is_valid():
            vehicle = Vehicle.objects.create(**serializer.validated_data)
            vehicle.save()
            response_serializer = GetVehiclesSerializer(vehicle)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OfficersViewSet(viewsets.ModelViewSet):
    queryset = Officer.objects.all()
    serializer_class = OfficersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Officer.objects.all()
        serializer = GetOfficersSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Officer.objects.all()
        try:
            officer = get_object_or_404(queryset, pk=pk)
        except ValidationError:
            raise NotFound("Officer not found")
        else:
            serializer = GetOfficersSerializer(officer)
            return Response(serializer.data)

    def create(self, request):
        serializer = OfficersSerializer(data=request.data)
        if serializer.is_valid():
            officer = Officer.objects.create(**serializer.validated_data)
            officer.save()
            response_serializer = GetOfficersSerializer(officer)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = Ticket.objects.all()
        serializer = GetTicketsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Ticket.objects.all()
        try:
            ticket = get_object_or_404(queryset, pk=pk)
        except ValidationError:
            raise NotFound("Ticket not found")
        else:
            serializer = GetTicketsSerializer(ticket)
            return Response(serializer.data)

    def create(self, request):
        serializer = CreateTicketsSerializer(data=request.data)
        if serializer.is_valid():
            vehicles_queryset = Vehicle.objects.all()
            vehicle = get_object_or_404(vehicles_queryset, plate=serializer.validated_data["plate"])

            officers_queryset = Officer.objects.all()
            officer = get_object_or_404(officers_queryset, person__user=self.request.user)

            ticket = Ticket.objects.create(
                vehicle=vehicle,
                reporting_officer=officer,
                notes=serializer.validated_data["notes"]
            )

            response_serializer = GetTicketsSerializer(ticket)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)


class GenerateInformViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request):
        serializer = GenerateInformsSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = Ticket.objects.filter(vehicle__owner__email=serializer.validated_data["email"])
            serializer = GetTicketsSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=404)
