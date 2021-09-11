from django.urls import path
from . import views, auth
urlpatterns = [
    path('travels', auth.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels/destination/<int:id>', auth.view),
    path('travels/add', auth.add),
    path('travels/add_trip', auth.add_trip),
    path('travels/join/{{user.id}}', auth.join),
]
