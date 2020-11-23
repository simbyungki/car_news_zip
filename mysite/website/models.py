from django.conf import settings
from django.db import models
from django.utils import timezone

class TblNewCarNewsList(models.Model):
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True, verbose_name='언론사')  # Field name made lowercase.
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)  # Field name made lowercase.
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True, verbose_name='기사 제목')  # Field name made lowercase.
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True, verbose_name='간추린 내용')  # Field name made lowercase.
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True, verbose_name='뉴스 링크 URL')  # Field name made lowercase.
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEW_CAR_NEWS_LIST'
		verbose_name = '신차 뉴스 ZIP'
		verbose_name_plural = '신차 뉴스 ZIP'


class TblNewKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
	positive_yn = models.CharField(db_column='POSITIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	negative_yn = models.CharField(db_column='NEGATIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEW_KEYWORD_LIST'


class TblUsedCarNewsList(models.Model):
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True, verbose_name='언론사')  # Field name made lowercase.
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)  # Field name made lowercase.
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True, verbose_name='기사 제목')  # Field name made lowercase.
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True, verbose_name='간추린 내용')  # Field name made lowercase.
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True, verbose_name='뉴스 링크 URL')  # Field name made lowercase.
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_USED_CAR_NEWS_LIST'
		verbose_name = '중고차 뉴스 ZIP'
		verbose_name_plural = '중고차 뉴스 ZIP'		


class TblUsedKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
	positive_yn = models.CharField(db_column='POSITIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	negative_yn = models.CharField(db_column='NEGATIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_USED_KEYWORD_LIST'
	
class TblReviewList(models.Model):
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True, verbose_name='언론사')  # Field name made lowercase.
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)  # Field name made lowercase.
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True, verbose_name='기사 제목')  # Field name made lowercase.
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True, verbose_name='간추린 내용')  # Field name made lowercase.
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True, verbose_name='뉴스 링크 URL')  # Field name made lowercase.
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_REVIEW_LIST'
		verbose_name = '시승기 ZIP'
		verbose_name_plural = '시승기 ZIP'	

class TblIndustryList(models.Model):
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True, verbose_name='언론사')  # Field name made lowercase.
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)  # Field name made lowercase.
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True, verbose_name='기사 제목')  # Field name made lowercase.
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True, verbose_name='간추린 내용')  # Field name made lowercase.
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True, verbose_name='뉴스 링크 URL')  # Field name made lowercase.
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_INDUSTRY_LIST'
		verbose_name = '자동차 업계 뉴스 ZIP'
		verbose_name_plural = '자동차 업계 뉴스 ZIP'	
