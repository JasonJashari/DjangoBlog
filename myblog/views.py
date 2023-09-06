from django.views.generic import ListView

from blog.models import Entry


class HomeView(ListView):

    model = Entry
    template_name = 'index.html'
    ordering = ['-created_at']