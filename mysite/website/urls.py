from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('/', views.news_list, name='news_list'),
	path('reload_data/', views.reload_data, name='reload_data'),
	path('login/', views.login, name='login'),
	path('join/', views.join, name='join')
]
