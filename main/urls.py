from django.urls import path

from main.views import index, category

app_name = 'main'
urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', category, name='category'),
]