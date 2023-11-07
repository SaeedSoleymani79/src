from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User

# Create your views here.

def search_view(request):
    return render(request, 'search/search.html')

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            users = User.objects.filter(username__istartswith=query)
            users_json = [{'username': user.username, 'url': request.build_absolute_uri(reverse('profile', kwargs={'username': user.username}))} for user in users]
            return JsonResponse(users_json, safe=False)
        else:
            return JsonResponse([], safe=False)