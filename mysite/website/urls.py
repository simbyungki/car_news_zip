from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('news_list', views.news_list, name='news_list'),
	path('news_detail', views.news_detail, name='news_detail'),
	path('search_result_list/', views.news_list, name='search_result_list'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('join/', views.join, name='join'),
	path('car_comments/', views.car_comments, name='car_comments'),
	path('list_data', views.list_data, name='list_data'),
	path('view_count', views.view_count, name='view_count'),
]
