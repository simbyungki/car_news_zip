from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('news_list', views.news_list, name='news_list'),
	path('news_detail', views.news_detail, name='news_detail'),
	path('new_news_detail', views.new_news_detail, name='new_news_detail'),
	path('news_trend', views.news_trend, name='news_trend'),
	path('search_result_list/', views.news_list, name='search_result_list'),
	path('car_review_list', views.car_review_list, name='car_review_list'),
	path('car_review_detail', views.car_review_detail, name='car_review_detail'),
	path('news_list_data', views.news_list_data, name='news_list_data'),
	path('car_review_list_data', views.car_review_list_data, name='car_review_list_data'),
	path('bobaecomm_data', views.bobaecomm_data, name='bobaecomm_data'),
	path('view_count', views.view_count, name='view_count'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('join/', views.join, name='join'),
	path('bobaenews/', views.bobaenews, name='bobarnews'),
	path('bobaecomm/', views.bobaecomm, name='bobaecomm')
]
