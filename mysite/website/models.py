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

class TblCarInfos(models.Model):
	info_no = models.AutoField(db_column='INFO_NO', primary_key=True)  # Field name made lowercase.
	bmname = models.CharField(db_column='BMNAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	boiname = models.CharField(db_column='BOINAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	boname = models.CharField(db_column='BONAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	bono = models.IntegerField(db_column='BONO', blank=True, null=True)  # Field name made lowercase.
	daum_code = models.CharField(db_column='DAUM_CODE', max_length=100, blank=True, null=True)  # Field name made lowercase.
	car_img_url = models.CharField(db_column='CAR_IMG_URL', max_length=300, blank=True, null=True)  # Field name made lowercase.
	car_price = models.CharField(db_column='CAR_PRICE', max_length=100, blank=True, null=True)  # Field name made lowercase.
	fuel_efficiency = models.CharField(db_column='FUEL_EFFICIENCY', max_length=100, blank=True, null=True)  # Field name made lowercase.
	car_cc = models.CharField(db_column='CAR_CC', max_length=100, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CAR_INFOS'

class TblNewsAllKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=500, blank=True, null=True)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
	media_code = models.CharField(db_column='MEDIA_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	mining_obj = models.CharField(db_column='MINING_OBJ', max_length=10, blank=True, null=True)  # Field name made lowercase.
	news_no = models.IntegerField(db_column='NEWS_NO', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEWS_ALL_KEYWORD_LIST'

class TblNewsKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', unique=True, max_length=500)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=100, blank=True, null=True)  # Field name made lowercase.
	mining_yn = models.CharField(db_column='MINING_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	positive_yn = models.CharField(db_column='POSITIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	negative_yn = models.CharField(db_column='NEGATIVE_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
	natural_yn = models.CharField(db_column='NATURAL_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
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
	title_mining_status = models.CharField(db_column='TITLE_MINING_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
	view_count = models.IntegerField(db_column='VIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
	origin_view_count = models.IntegerField(db_column='ORIGIN_VIEW_COUNT', blank=True, null=True)  # Field name made lowercase.
	reporter_name = models.CharField(db_column='REPORTER_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
	mining_date = models.DateTimeField(db_column='MINING_DATE', blank=True, null=True)  # Field name made lowercase.
	title_mining_date = models.DateTimeField(db_column='TITLE_MINING_DATE', blank=True, null=True)  # Field name made lowercase.
	positive_count = models.IntegerField(db_column='POSITIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
	negative_count = models.IntegerField(db_column='NEGATIVE_COUNT', blank=True, null=True)  # Field name made lowercase.
	va_count = models.IntegerField(db_column='VA_COUNT', blank=True, null=True)  # Field name made lowercase.
	morpheme_count = models.IntegerField(db_column='MORPHEME_COUNT', blank=True, null=True)  # Field name made lowercase.
	proc_status = models.CharField(db_column='PROC_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
	writer_name = models.CharField(db_column='WRITER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
	car_model_bat_status = models.IntegerField(db_column='CAR_MODEL_BAT_STATUS')  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_TOTAL_CAR_NEWS_LIST'

class TblNewsCarModelMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	bono = models.IntegerField(db_column='BONO', blank=True, null=True)  # Field name made lowercase.
	boname = models.CharField(db_column='BONAME', max_length=500, blank=True, null=True)  # Field name made lowercase.
	news_no = models.IntegerField(db_column='NEWS_NO', blank=True, null=True)  # Field name made lowercase.
	map_date = models.DateTimeField(db_column='MAP_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_NEWS_CAR_MODEL_MAP'

class TblYoutubeCarCommentList(models.Model):
	comment_no = models.AutoField(db_column='COMMENT_NO', primary_key=True)  # Field name made lowercase.
	comment_video_id = models.CharField(db_column='COMMENT_VIDEO_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
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
	writer_name = models.CharField(db_column='WRITER_NAME', max_length=200, blank=True, null=True)  # Field name made lowercase.
	info_no = models.IntegerField(db_column='INFO_NO')  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_YOUTUBE_CAR_COMMENT_LIST'

class TblCcqBigramMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	qna_no = models.IntegerField(db_column='QNA_NO', unique=True)  # Field name made lowercase.
	q_category = models.IntegerField(db_column='Q_CATEGORY', blank=True, null=True)  # Field name made lowercase.
	bigrams = models.TextField(db_column='BIGRAMS', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CCQ_BIGRAM_MAP'


class TblCcqKeywordBigramMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	qna_no = models.IntegerField(db_column='QNA_NO', unique=True)  # Field name made lowercase.
	q_category = models.IntegerField(db_column='Q_CATEGORY', blank=True, null=True)  # Field name made lowercase.
	bigrams = models.TextField(db_column='BIGRAMS', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CCQ_KEYWORD_BIGRAM_MAP'


class TblCcqKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	qna_no = models.CharField(db_column='QNA_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
	word_origin = models.CharField(db_column='WORD_ORIGIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_class_code = models.IntegerField(db_column='WORD_CLASS_CODE', blank=True, null=True)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=50, blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CCQ_KEYWORD_LIST'


class TblCcqKeywordMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	qna_no = models.IntegerField(db_column='QNA_NO', blank=True, null=True)  # Field name made lowercase.
	source_word_no = models.IntegerField(db_column='SOURCE_WORD_NO', blank=True, null=True)  # Field name made lowercase.
	source_word = models.CharField(db_column='SOURCE_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	source_class_code = models.CharField(db_column='SOURCE_CLASS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	source_morpheme_word = models.CharField(db_column='SOURCE_MORPHEME_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_word_no = models.IntegerField(db_column='TARGET_WORD_NO', blank=True, null=True)  # Field name made lowercase.
	target_word = models.CharField(db_column='TARGET_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_class_code = models.CharField(db_column='TARGET_CLASS_CODE', max_length=30, blank=True, null=True)  # Field name made lowercase.
	target_morpheme_word = models.CharField(db_column='TARGET_MORPHEME_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_distance = models.IntegerField(db_column='WORD_DISTANCE', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.
	distance_weight = models.FloatField(db_column='DISTANCE_WEIGHT', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CCQ_KEYWORD_MAP'


class TblCcqQTypeInfo(models.Model):
	type_no = models.AutoField(db_column='TYPE_NO', primary_key=True)  # Field name made lowercase.
	q_type_code = models.IntegerField(db_column='Q_TYPE_CODE', unique=True)  # Field name made lowercase.
	q_type_name = models.CharField(db_column='Q_TYPE_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_CCQ_Q_TYPE_INFO'

class TblAnalWordClass(models.Model):
	word_class_code = models.IntegerField(db_column='WORD_CLASS_CODE', primary_key=True)  # Field name made lowercase.
	class_name = models.CharField(db_column='CLASS_NAME', unique=True, max_length=30)  # Field name made lowercase.
	kor_class_name = models.CharField(db_column='KOR_CLASS_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
	status = models.IntegerField(db_column='STATUS', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_ANAL_WORD_CLASS'


class TblBobaeKeywordDistanceMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	source_word = models.CharField(db_column='SOURCE_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_word = models.CharField(db_column='TARGET_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_distance = models.IntegerField(db_column='WORD_DISTANCE', blank=True, null=True)  # Field name made lowercase.
	distance_weight = models.DecimalField(db_column='DISTANCE_WEIGHT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_BOBAE_KEYWORD_DISTANCE_MAP'


class TblBobaeKeywordList(models.Model):
	word_no = models.AutoField(db_column='WORD_NO', primary_key=True)  # Field name made lowercase.
	post_code = models.CharField(db_column='POST_CODE', max_length=30)  # Field name made lowercase.
	word_origin = models.CharField(db_column='WORD_ORIGIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_morpheme = models.CharField(db_column='WORD_MORPHEME', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_class_code = models.CharField(db_column='WORD_CLASS_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_class = models.CharField(db_column='WORD_CLASS', max_length=50, blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_BOBAE_KEYWORD_LIST'


class TblBobaeKeywordMap(models.Model):
	map_no = models.AutoField(db_column='MAP_NO', primary_key=True)  # Field name made lowercase.
	source_word_no = models.IntegerField(db_column='SOURCE_WORD_NO', blank=True, null=True)  # Field name made lowercase.
	source_word = models.CharField(db_column='SOURCE_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	source_class_code = models.CharField(db_column='SOURCE_CLASS_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	source_morpheme_word = models.CharField(db_column='SOURCE_MORPHEME_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_word_no = models.IntegerField(db_column='TARGET_WORD_NO', blank=True, null=True)  # Field name made lowercase.
	target_word = models.CharField(db_column='TARGET_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_class_code = models.CharField(db_column='TARGET_CLASS_CODE', max_length=50, blank=True, null=True)  # Field name made lowercase.
	target_morpheme_word = models.CharField(db_column='TARGET_MORPHEME_WORD', max_length=50, blank=True, null=True)  # Field name made lowercase.
	word_distance = models.IntegerField(db_column='WORD_DISTANCE', blank=True, null=True)  # Field name made lowercase.
	distance_weight = models.IntegerField(db_column='DISTANCE_WEIGHT', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_BOBAE_KEYWORD_MAP'


class TblBobaePostCodeList(models.Model):
	post_no = models.AutoField(db_column='POST_NO', primary_key=True)  # Field name made lowercase.
	post_code = models.CharField(db_column='POST_CODE', unique=True, max_length=30)  # Field name made lowercase.
	url = models.CharField(db_column='URL', max_length=100, blank=True, null=True)  # Field name made lowercase.
	view_cnt = models.IntegerField(db_column='VIEW_CNT', blank=True, null=True)  # Field name made lowercase.
	recommend_cnt = models.IntegerField(db_column='RECOMMEND_CNT', blank=True, null=True)  # Field name made lowercase.
	mining_status = models.IntegerField(db_column='MINING_STATUS', blank=True, null=True)  # Field name made lowercase.
	mining_date = models.DateTimeField(db_column='MINING_DATE', blank=True, null=True)  # Field name made lowercase.
	update_date = models.DateTimeField(db_column='UPDATE_DATE', blank=True, null=True)  # Field name made lowercase.

	class Meta:
		managed = False
		db_table = 'TBL_BOBAE_POST_CODE_LIST'