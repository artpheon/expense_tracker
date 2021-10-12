from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from restapi import models, serializers

# Create your views here.


class ExpenseListCreate(ListCreateAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()


class ExpenseRetrieveDelete(RetrieveDestroyAPIView):
    serializer_class = serializers.Expense
    queryset = models.Expense.objects.all()
