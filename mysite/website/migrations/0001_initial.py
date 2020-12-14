# Generated by Django 3.1.4 on 2020-12-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblTotalCarNewsList',
            fields=[
                ('news_no', models.AutoField(db_column='NEWS_NO', primary_key=True, serialize=False)),
                ('news_category', models.CharField(blank=True, db_column='NEWS_CATEGORY', max_length=10, null=True, verbose_name='뉴스 카테고리')),
                ('media_code', models.CharField(blank=True, db_column='MEDIA_CODE', max_length=50, null=True)),
                ('media_name', models.CharField(blank=True, db_column='MEDIA_NAME', max_length=100, null=True, verbose_name='언론사')),
                ('news_code', models.CharField(db_column='NEWS_CODE', max_length=100, unique=True)),
                ('news_title', models.CharField(blank=True, db_column='NEWS_TITLE', max_length=1000, null=True, verbose_name='기사 제목')),
                ('news_summary', models.TextField(blank=True, db_column='NEWS_SUMMARY', null=True, verbose_name='간추린 내용')),
                ('news_content', models.TextField(blank=True, db_column='NEWS_CONTENT', null=True, verbose_name='기사 상세')),
                ('news_img_url', models.CharField(blank=True, db_column='NEWS_IMG_URL', max_length=1000, null=True)),
                ('news_url', models.CharField(blank=True, db_column='NEWS_URL', max_length=1000, null=True, verbose_name='뉴스 링크 URL')),
                ('write_date', models.CharField(blank=True, db_column='WRITE_DATE', max_length=30, null=True)),
                ('add_date', models.DateTimeField(blank=True, db_column='ADD_DATE', null=True)),
                ('mining_status', models.CharField(blank=True, db_column='MINING_STATUS', max_length=10, null=True, verbose_name='텍스트 마이닝 여부')),
            ],
            options={
                'verbose_name': '자동차 뉴스 ZIP',
                'verbose_name_plural': '자동차 뉴스 ZIP',
                'db_table': 'TBL_TOTAL_CAR_NEWS_LIST',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TblMemberList',
            fields=[
                ('memb_no', models.AutoField(db_column='MEMB_NO', primary_key=True, serialize=False, verbose_name='No')),
                ('memb_id', models.EmailField(db_column='MEMB_ID', max_length=100, verbose_name='아이디')),
                ('memb_name', models.CharField(db_column='MEMB_NAME', max_length=100, verbose_name='이름')),
                ('gender', models.CharField(db_column='MEMB_GENDER', max_length=10, verbose_name='성별')),
                ('password', models.CharField(db_column='PASSWORD', max_length=100, verbose_name='비밀번호')),
                ('add_date', models.DateTimeField(auto_now_add=True, db_column='ADD_DATE', verbose_name='가입일시')),
            ],
            options={
                'verbose_name': '회원',
                'verbose_name_plural': '회원',
                'db_table': 'TBL_MEMBER_LIST',
            },
        ),
    ]
