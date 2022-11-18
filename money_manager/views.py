from django.contrib.auth.models import User
import django_filters
from django_filters import filters
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from money_manager.seriazlizer import TransactionSerializer, CategorySerializer, ProfileSerializer, \
    RegistrationSerializer
from money_manager.models import Transaction, Category, Balance


class DateTimeFilter(django_filters.FilterSet, OrderingFilter):
    date = filters.DateFilter(field_name='date_of_transaction', label='date')
    date_to = filters.DateFilter(field_name='date_of_transaction', label='date_to', lookup_expr='lte')
    date_from = filters.DateFilter(field_name='date_of_transaction', label='date_from', lookup_expr='gte')
    time = filters.TimeFilter(field_name='time_of_transaction', label='time')
    time_to = filters.TimeFilter(field_name='time_of_transaction', label='time_to', lookup_expr='lte')
    time_from = filters.TimeFilter(field_name='time_of_transaction', label='time_from', lookup_expr='gte')
    ordering_fields = ('date_of_transaction', 'time_of_transaction')
    amount = filters.TimeFilter(field_name='amount_of_transaction', label='amount')
    amount_to = filters.TimeFilter(field_name='amount_of_transaction', label='amount_to', lookup_expr='lte')
    amount_from = filters.TimeFilter(field_name='amount_of_transaction', label='amount_from', lookup_expr='gte')

    class Meta:
        model = Transaction
        fields = ['date', ]


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAuthenticated,)
    filter_class = DateTimeFilter
    # filter_backends = (DjangoFilterBackend, OrderingFilter,)
    # filter_fields = ('date_of_transaction', 'time_of_transaction')
    ordering_fields = ('date_of_transaction', 'time_of_transaction', 'amount_of_transaction', )

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user.id)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user.id)
        return queryset


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def list(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=self.request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Balance.objects.filter(user=self.request.user.id)
        return queryset
