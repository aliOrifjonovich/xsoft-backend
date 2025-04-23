from rest_framework import viewsets
from app.models.client import Client
from app.models.employee import Employee
from users.models import User
from rest_framework import status
from rest_framework.response import Response
from ..models.cars import Car,CarImages,CarFeatures,CarCategory
from app.serializers.client import CleintSerializer,ClientCreateSerializer
from ..pagination .paginations import DefaultLimitOffSetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Sum

class CarStatistics(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get car statistics",
        responses={
            200: openapi.Response(
                description="Car statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_cars': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of cars'),
                        'free_cars': openapi.Schema(type=openapi.TYPE_INTEGER, description='Available cars'),
                        'on_rent_cars': openapi.Schema(type=openapi.TYPE_INTEGER, description='Currently rented cars'),
                        'reserved_cars': openapi.Schema(type=openapi.TYPE_INTEGER, description='Reserved cars'),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
        }
    )

    def get(self, request, *args, **kwargs):
        total_cars = Car.objects.count()
        
        # Get count of cars by rental status
        free_cars = Car.objects.filter(rental_status=Car.RENTAL_STATUS_CHOICES.BOSH).count()
        on_rent_cars = Car.objects.filter(rental_status=Car.RENTAL_STATUS_CHOICES.IJARADA).count()
        reserved_cars = Car.objects.filter(rental_status=Car.RENTAL_STATUS_CHOICES.RESERV).count()
        
        # Prepare response data
        data = {
            'total_cars': total_cars,
            'free_cars': free_cars,
            'on_rent_cars': on_rent_cars,
            'reserved_cars': reserved_cars,
        }
        
        return Response(data, status=status.HTTP_200_OK)

class ClientStatisticsAPIView(APIView):
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get client statistics",
        responses={
            200: openapi.Response(
                description="Client statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_clients': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total clients'),
                        'active_clients': openapi.Schema(type=openapi.TYPE_INTEGER, description='Active clients'),
                        'passive_clients': openapi.Schema(type=openapi.TYPE_INTEGER, description='Inactive clients'),
                        'blacklisted_clients': openapi.Schema(type=openapi.TYPE_INTEGER, description='Blacklisted clients'),
                    }
                )
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Returns statistics about clients:
        - total_clients
        - active_clients
        - passive_clients
        - blacklisted_clients
        """
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(
            status=Client.STATUS_CHOICES.Active
        ).count()
        passive_clients = Client.objects.filter(
            status=Client.STATUS_CHOICES.InActive
        ).count()
        blacklisted_clients = Client.objects.filter(
            status=Client.STATUS_CHOICES.BLACKLISTED
        ).count()

        data = {
            'total_clients': total_clients,
            'active_clients': active_clients,
            'passive_clients': passive_clients,
            'blacklisted_clients': blacklisted_clients,
        }
        
        return Response(data, status=status.HTTP_200_OK)


class EmployeeStatisticsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Get employee statistics",
        responses={
            200: openapi.Response(
                description="Employee statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_staffs': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total employees'),
                        'total_salary': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Total salary sum'),
                        'active_staffs': openapi.Schema(type=openapi.TYPE_INTEGER, description='Active employees'),
                        'staffs_on_vacation': openapi.Schema(type=openapi.TYPE_INTEGER, description='Employees on vacation'),
                    }
                )
            ),
            401: openapi.Response(
            description="Unauthorized",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),        
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Returns statistics about employees:
        - total_staffs: Total number of employees
        - total_salary: Sum of all employees' salaries
        - active_staffs: Employees with 'Active' work status
        - staffs_on_vacation: Employees with 'Vacation' work status
        """
        # Total number of employees
        total_staffs = Employee.objects.count()
        
        # Total salary sum (excluding fired employees)
        total_salary = Employee.objects.exclude(
            workStatus=Employee.WORK_STATUS_CHOICES.FIRED
        ).aggregate(total_salary=Sum('salary'))['total_salary'] or 0
        
        # Active employees count
        active_staffs = Employee.objects.filter(
            workStatus=Employee.WORK_STATUS_CHOICES.Active
        ).count()
        
        # Employees on vacation count
        staffs_on_vacation = Employee.objects.filter(
            workStatus=Employee.WORK_STATUS_CHOICES.VACATION
        ).count()

        data = {
            'total_staffs': total_staffs,
            'total_salary': float(total_salary),  # Convert Decimal to float for JSON serialization
            'active_staffs': active_staffs,
            'staffs_on_vacation': staffs_on_vacation,
        }
        
        return Response(data, status=status.HTTP_200_OK)