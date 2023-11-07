from django.urls import path
from .views import SearchView, search_view

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('user/', search_view, name='searchtmpl')
]
