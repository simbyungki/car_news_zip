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


class TblNewsKeywordList(models.Model):
    word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
    word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=500, blank=True, null=True)  # Field name made lowercase.
    word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    positive_yn = models.CharField(db_column='POSITIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    negative_yn = models.CharField(db_column='NEGATIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TBL_NEWS_KEYWORD_LIST'


class TblNewsKeywordMap(models.Model):
    map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
    word_origin = models.CharField(db_column='WORD_ORIGIN', max_length=500, blank=True, null=True)  # Field name made lowercase.
    word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=500, blank=True, null=True)  # Field name made lowercase.
    news_no = models.IntegerField(db_column='NEWS_NO', blank=True, null=True)  # Field name made lowercase.
    word_count = models.IntegerField(db_column='WORD_COUNT', blank=True, null=True)  # Field name made lowercase.

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
    reporter_name = models.CharField(db_column='REPORTER_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase. 
    view_count = models.IntegerField(db_column='VIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
    news_img_url = models.CharField(db_column='NEWS_IMG_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    news_url = models.CharField(db_column='NEWS_URL', max_length=1000, blank=True, null=True)  # Field name made lowercase.        
    write_date = models.CharField(db_column='WRITE_DATE', max_length=30, blank=True, null=True)  # Field name made lowercase.      
    add_date = models.DateTimeField(db_column='ADD_DATE', blank=True, null=True)  # Field name made lowercase.
    mining_status = models.CharField(db_column='MINING_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mining_date = models.DateTimeField(db_column='MINING_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TBL_TOTAL_CAR_NEWS_LIST'