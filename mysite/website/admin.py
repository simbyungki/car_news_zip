from django.contrib import admin
from .models import TblTotalCarNewsList
from .models import TblMemberList

class newsList(admin.ModelAdmin) :
	list_display = ['news_no', 'news_category', 'media_name', 'news_title', 'write_date']

class memberList(admin.ModelAdmin) :
	list_display = ['memb_name', 'memb_id', 'gender', 'add_date', 'memb_no']

admin.site.register(TblTotalCarNewsList, newsList)
admin.site.register(TblMemberList, memberList)


