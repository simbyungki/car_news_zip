from django.contrib import admin
from .models import TblUsedCarNewsList
from .models import TblNewCarNewsList
from .models import TblReviewList
from .models import TblIndustryList
from .models import TblMemberList

class newsList(admin.ModelAdmin) :
	list_display = ['news_no', 'media_name', 'news_title', 'write_date']

class memberList(admin.ModelAdmin) :
	list_display = ['memb_name', 'memb_id', 'gender', 'add_date', 'memb_no']

admin.site.register(TblUsedCarNewsList, newsList)
admin.site.register(TblNewCarNewsList, newsList)
admin.site.register(TblReviewList, newsList)
admin.site.register(TblIndustryList, newsList)
admin.site.register(TblMemberList, memberList)


