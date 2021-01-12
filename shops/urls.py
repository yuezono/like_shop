from django.urls import path

from . import views

app_name = 'shops'
urlpatterns = [
  path('', views.IndexView.as_view(),name='index'),
  path('inquiry/',views.InquiryView.as_view(),name='inquiry'),
  path('shops-list/',views.ShopsListView.as_view(),name='shops_list'),
  path('shops-detail/<int:pk>/',views.ShopsDetailView.as_view(),name='shops_detail'),
  path('shops-create/',views.ShopsCreateView.as_view(),name='shops_create'),
  path('shops-update/<int:pk>/',views.ShopsUpdateView.as_view(),name='shops_update'),
  path('shops-delete/<int:pk>/',views.ShopsDeleteView.as_view(),name='shops_delete'),
]