from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^start/', views.StartView.as_view(), name='start'),
    url(r'^read/', views.ReadView.as_view(), name='read'),
    url(r'^rating/', views.RatingView.as_view(), name='rating'),
]