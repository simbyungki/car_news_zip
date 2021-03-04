from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('news_list', views.news_list, name='news_list'),
	path('news_detail', views.news_detail, name='news_detail'),
	path('news_trend', views.news_trend, name='news_trend'),
	path('search_result_list/', views.news_list, name='search_result_list'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('join/', views.join, name='join'),
	path('car_comments/', views.car_comments, name='car_comments'),
	path('news_list_data', views.news_list_data, name='news_list_data'),
	path('car_comment_list_data', views.car_comment_list_data, name='car_comment_list_data'),
	path('view_count', views.view_count, name='view_count'),
]
