from django.urls import path

from . import views

app_name = 'shops'
urlpatterns = [
  path('', views.IndexView.as_view(),name='index'),
  path('inquiry/',views.InquiryView.as_view(),name='inquiry'),
  path('shops-list/',views.ShopsListView.as_view(),name='shops_list'),
]
