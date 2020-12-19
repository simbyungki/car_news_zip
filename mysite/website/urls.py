from django.urls import path
from . import views

urlpatterns = [
	path('', views.news_list, name='news_list'),
	path('news_list', views.news_list, name='news_list'),
	path('reload_list_data/', views.reload_list_data, name='reload_list_data'),
	path('load_detail_data/', views.load_detail_data, name='load_detail_data'),
	path('text_mining_result/', views.text_mining_result, name='text_mining_result'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('join/', views.join, name='join'),
	path('list_data', views.list_data, name='list_data'),
	path('view_count', views.view_count, name='view_count'),
	path('text_mining/', views.text_mining, name='text_mining'),
]
