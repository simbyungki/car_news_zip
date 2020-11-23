# Generated by Django 2.0.13 on 2020-11-18 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblNewCarNewsList',
            fields=[
                ('news_no', models.AutoField(db_column='NEWS_NO', primary_key=True, serialize=False)),
                ('media_code', models.CharField(blank=True, db_column='MEDIA_CODE', max_length=50, null=True)),
                ('media_name', models.CharField(blank=True, db_column='MEDIA_NAME', max_length=100, null=True, verbose_name='언론사')),
                ('news_code', models.CharField(db_column='NEWS_CODE', max_length=100, unique=True)),
                ('news_title', models.CharField(blank=True, db_column='NEWS_TITLE', max_length=1000, null=True, verbose_name='기사 제목')),
                ('news_content', models.TextField(blank=True, db_column='NEWS_CONTENT', null=True, verbose_name='간추린 내용')),
                ('news_img_url', models.CharField(blank=True, db_column='NEWS_IMG_URL', max_length=1000, null=True)),
                ('news_url', models.CharField(blank=True, db_column='NEWS_URL', max_length=1000, null=True, verbose_name='뉴스 링크 URL')),
                ('write_date', models.CharField(blank=True, db_column='WRITE_DATE', max_length=30, null=True)),
                ('add_date', models.DateTimeField(blank=True, db_column='ADD_DATE', null=True)),
            ],
            options={
                'verbose_name': '중고차 뉴스 ZIP',
                'verbose_name_plural': '중고차 뉴스 ZIP',
                'db_table': 'TBL_NEW_CAR_NEWS_LIST',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblNewKeywordList',
            fields=[
                ('word_no', models.AutoField(db_column='WORD_NO', primary_key=True, serialize=False)),
                ('word_morpheme', models.CharField(blank=True, db_column='WORD_MORPHEME', max_length=100, null=True)),
                ('word_class', models.CharField(blank=True, db_column='WORD_CLASS', max_length=100, null=True)),
                ('positive_yn', models.CharField(blank=True, db_column='POSITIVE_YN', max_length=1, null=True)),
                ('negative_yn', models.CharField(blank=True, db_column='NEGATIVE_YN', max_length=1, null=True)),
            ],
            options={
                'db_table': 'TBL_NEW_KEYWORD_LIST',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsedCarNewsList',
            fields=[
                ('news_no', models.AutoField(db_column='NEWS_NO', primary_key=True, serialize=False)),
                ('media_code', models.CharField(blank=True, db_column='MEDIA_CODE', max_length=50, null=True)),
                ('media_name', models.CharField(blank=True, db_column='MEDIA_NAME', max_length=100, null=True, verbose_name='언론사')),
                ('news_code', models.CharField(db_column='NEWS_CODE', max_length=100, unique=True)),
                ('news_title', models.CharField(blank=True, db_column='NEWS_TITLE', max_length=1000, null=True, verbose_name='기사 제목')),
                ('news_content', models.TextField(blank=True, db_column='NEWS_CONTENT', null=True, verbose_name='간추린 내용')),
                ('news_img_url', models.CharField(blank=True, db_column='NEWS_IMG_URL', max_length=1000, null=True)),
                ('news_url', models.CharField(blank=True, db_column='NEWS_URL', max_length=1000, null=True, verbose_name='뉴스 링크 URL')),
                ('write_date', models.CharField(blank=True, db_column='WRITE_DATE', max_length=30, null=True)),
                ('add_date', models.DateTimeField(blank=True, db_column='ADD_DATE', null=True)),
            ],
            options={
                'verbose_name': '신차 뉴스 ZIP',
                'verbose_name_plural': '신차 뉴스 ZIP',
                'db_table': 'TBL_USED_CAR_NEWS_LIST',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblUsedKeywordList',
            fields=[
                ('word_no', models.AutoField(db_column='WORD_NO', primary_key=True, serialize=False)),
                ('word_morpheme', models.CharField(blank=True, db_column='WORD_MORPHEME', max_length=100, null=True)),
                ('word_class', models.CharField(blank=True, db_column='WORD_CLASS', max_length=100, null=True)),
                ('positive_yn', models.CharField(blank=True, db_column='POSITIVE_YN', max_length=1, null=True)),
                ('negative_yn', models.CharField(blank=True, db_column='NEGATIVE_YN', max_length=1, null=True)),
            ],
            options={
                'db_table': 'TBL_USED_KEYWORD_LIST',
                'managed': False,
            },
        ),
    ]