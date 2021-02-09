from django.conf import settings
from django.db import models
from django.utils import timezone

class TblMemberList(models.Model):
	memb_no = models.AutoField(db_column='MEMB_NO', primary_key=True)  # Field name made lowercase.
	memb_id = models.CharField(db_column='MEMB_ID', max_length=100)  # Field name made lowercase.
	memb_gender = models.CharField(db_column='MEMB_GENDER', max_length=10)  # Field name made lowercase.
	password = models.CharField(db_column='PASSWORD', max_length=100)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE')  # Field name made lowercase.
	memb_name = models.CharField(db_column='MEMB_NAME', max_length=100)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_MEMBER_LIST'

class LogConnectList(models.Model):
	log_no = models.AutoField(db_column='LOG_NO', primary_key=True)  # Field name made lowercase.
	page_name = models.CharField(db_column='PAGE_NAME', max_length=500, blank=True, null=True)  # Field name made lowercase.    
	referer_url = models.CharField(db_column='REFERER_URL', max_length=500, blank=True, null=True)  # Field name made lowercase.
	user_ip = models.CharField(db_column='USER_IP', max_length=30, blank=True, null=True)  # Field name made lowercase.
	connect_ymd = models.CharField(db_column='CONNECT_YMD', max_length=30, blank=True, null=True)  # Field name made lowercase.
	connect_time = models.CharField(db_column='CONNECT_TIME', max_length=30, blank=True, null=True)  # Field name made lowercase.
	connect_date = models.DateTimeField(db_column='CONNECT_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'LOG_CONNECT_LIST'

class LogSearchList(models.Model):
	log_no = models.AutoField(db_column='LOG_NO', primary_key=True)  # Field name made lowercase.
	search_word = models.CharField(db_column='SEARCH_WORD', max_length=500, blank=True, null=True)  # Field name made lowercase.
	search_return_count = models.IntegerField(db_column='SEARCH_RETURN_COUNT', blank=True, null=True)  # Field name made lowercase.
	searcher_ip = models.CharField(db_column='SEARCHER_IP', max_length=30, blank=True, null=True)  # Field name made lowercase.
	search_ymd = models.CharField(db_column='SEARCH_YMD', max_length=30, blank=True, null=True)  # Field name made lowercase.
	search_time = models.CharField(db_column='SEARCH_TIME', max_length=30, blank=True, null=True)  # Field name made lowercase.
	search_date = models.DateTimeField(db_column='SEARCH_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'LOG_SEARCH_LIST'

class TblNewsKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', unique=True, max_length=500)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
	positive_yn = models.CharField(db_column='POSITIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	negative_yn = models.CharField(db_column='NEGATIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEWS_KEYWORD_LIST'


class TblNewsKeywordMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	word_origin = models.CharField(db_column='WORD_ORIGIN', max_length=500, blank=True, null=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=500, blank=True, null=True)  # Field name made lowercase.
	news_no = models.IntegerField(db_column='NEWS_NO', blank=True, null=True)  # Field name made lowercase.
	word_count = models.IntegerField(db_column='WORD_COUNT', blank=True, null=True)  # Field name made lowercase.
	word_no = models.IntegerField(db_column='WORD_NO', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEWS_KEYWORD_MAP'


class TblTotalCarNewsList(models.Model):
	news_no = models.AutoField(db_column='NEWS_NO', primary_key=True)  # Field name made lowercase.
	news_category = models.IntegerField(db_column='NEWS_CATEGORY', blank=True, null=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	media_name = models.CharField(db_column='MEDIA_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	news_code = models.CharField(db_column='NEWS_CODE', unique=True, max_length=100)  # Field name made lowercase.
	news_title = models.CharField(db_column='NEWS_TITLE', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_summary = models.TextField(db_column='NEWS_SUMMARY', blank=True, null=True)  # Field name made lowercase.
	news_content = models.TextField(db_column='NEWS_CONTENT', blank=True, null=True)  # Field name made lowercase.
	news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
	write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.
	mining_status = models.CharField(db_column='MINING_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
	view_count = models.IntegerField(db_column='VIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
	reporter_name = models.CharField(db_column='REPORTER_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	mining_date = models.DateTimeField(db_column='MINING_DATE', blank=True, null=True)  # Field name made lowercase.
	positive_count = models.IntegerField(db_column='POSITIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
	negative_count = models.IntegerField(db_column='NEGATIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
	va_count = models.IntegerField(db_column='VA_COUNT', blank=True, null=True)  # Field name made lowercase.
	morpheme_count = models.IntegerField(db_column='MORPHEME_COUNT', blank=True, null=True)  # Field name made lowercase.
	proc_status = models.CharField(db_column='PROC_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_TOTAL_CAR_NEWS_LIST'


class TblYoutubeCarCommentList(models.Model):
    comment_no = models.AutoField(db_column='COMMENT_NO', primary_key=True)  # Field name made lowercase.
    comment_video_id = models.CharField(db_column='COMMENT_VIDEO_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bmname = models.CharField(db_column='BMNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    boiname = models.CharField(db_column='BOINAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    boname = models.CharField(db_column='BONAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bono = models.IntegerField(db_column='BONO', blank=True, null=True)  # Field name made lowercase.
    comment_content = models.TextField(db_column='COMMENT_CONTENT', blank=True, null=True)  # Field name made lowercase.
    comment_content_length = models.IntegerField(db_column='COMMENT_CONTENT_LENGTH', blank=True, null=True)  # Field name made lowercase.
    add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.
    minning_status = models.IntegerField(db_column='MINNING_STATUS', blank=True, null=True)  # Field name made lowercase.
    mining_date = models.DateTimeField(db_column='MINING_DATE', blank=True, null=True)  # Field name made lowercase.
    positive_count = models.IntegerField(db_column='POSITIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
    negative_count = models.IntegerField(db_column='NEGATIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
    va_count = models.IntegerField(db_column='VA_COUNT', blank=True, null=True)  # Field name made lowercase.
    morpheme_count = models.IntegerField(db_column='MORPHEME_COUNT', blank=True, null=True)  # Field name made lowercase.
    proc_status = models.IntegerField(db_column='PROC_STATUS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TBL_YOUTUBE_CAR_COMMENT_LIST'