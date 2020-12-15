from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('news_list', views.news_list, name='news_list'),
	path('reload_data/', views.reload_data, name='reload_data'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('join/', views.join, name='join'),
	path('list_data', views.list_data, name='list_data'),
	path('view_count', views.view_count, name='view_count'),
]
