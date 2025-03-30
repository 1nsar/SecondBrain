from django.shortcuts import render

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from .models import Entry  # Ensure Entry model is imported

# TEMPORARY FIX: If LockedView is missing, define a basic class
try:
    from .locked_view import LockedView  # If LockedView is in another file
except ImportError:
    class LockedView:  # Temporary fallback
        pass

class EntryListView(LockedView, ListView):
    model = Entry
    template_name = "entries/entry_list.html"


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Entry

from .models import Entry

class EntryListView(LockedView, ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")

class EntryDetailView(LockedView, DetailView):
    model = Entry

class EntryCreateView(LockedView, SuccessMessageMixin, CreateView):
    model = Entry
    fields = ["title", "content"]
    success_url = reverse_lazy("entry-list")
    success_message = "Your new entry was created!"

class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content"]
    success_message = "Your entry was updated!"

    def get_success_url(self):
        return reverse_lazy(
            "entry-detail",
            kwargs={"pk": self.object.pk}
        )

class EntryDeleteView(LockedView, SuccessMessageMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("entry-list")
    success_message = "Your entry was deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class LockedView(LoginRequiredMixin):
    login_url = "admin:login"