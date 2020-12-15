from django.conf import settings
from django.db import models
from django.utils import timezone


# 회원 TABLE
class TblMemberList(models.Model) :
	objects = models.Manager()
	memb_no = models.AutoField(db_column='MEMB_NO', primary_key=True, verbose_name='No')
	memb_id = models.EmailField(db_column='MEMB_ID', max_length=100, verbose_name='아이디')
	memb_name = models.CharField(db_column='MEMB_NAME', max_length=100, verbose_name='이름')
	gender = models.CharField(db_column='MEMB_GENDER', max_length=10, verbose_name='성별')
	password = models.CharField(db_column='PASSWORD', max_length=100, verbose_name='비밀번호')
	add_date = models.DateTimeField(db_column='ADD_DATE', auto_now_add=True, verbose_name='가입일시')
	class Meta : 
		db_table = 'TBL_MEMBER_LIST'
		verbose_name = '회원'
		verbose_name_plural = '회원'

# 통합 뉴스 TABLE
class TblTotalCarNewsList(models.Model):
	# objects = models.Manager()
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)
	news_category = models.CharField(db_column='NEWS_CATEGORY', max_length=10, blank=True, null=True, verbose_name='뉴스 카테고리')
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True, verbose_name='언론사')
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True, verbose_name='기사 제목')
	news_summary = models.TextField(db_column='NEWS_SUMMARY', blank=True, null=True, verbose_name='간추린 내용')
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True, verbose_name='기사 상세')
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True, verbose_name='뉴스 링크 URL')
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)
	mining_status = models.CharField(db_column='MINING_STATUS', max_length=10, blank=True, null=True, verbose_name='텍스트 마이닝 여부')
	view_count = models.CharField(db_column='VIEW_COUNT',  max_length=10, verbose_name='해당 기사 클릭 횟수')
	class Meta:
		managed = False
		db_table = 'TBL_TOTAL_CAR_NEWS_LIST'
		verbose_name = '자동차 뉴스.zip'
		verbose_name_plural = '자동차 뉴스.zip'