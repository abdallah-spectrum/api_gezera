from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateJournalItem.as_view(), name='journal_entry_create'),
    path('cancel/', views.CancelJournal.as_view(), name='journal_entry_create')
]
