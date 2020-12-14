from django.test import TestCase
from .models import TblTotalCarNewsList
# 뉴스 기사 상세 크롤링 > INSERT 
def get_auto_h_detail() :
	newsList = TblTotalCarNewsList.objects.all(media_code=1)

	print(newsList)

