from django.urls import path
from . import views


from django.http import HttpResponse

urlpatterns = [
    path('account_items_list/', views.AccountItemsList.as_view(), name='account_items_list')
]
