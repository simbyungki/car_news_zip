from django.shortcuts import render
from .models import TblUsedCarNewsList
from .models import TblNewCarNewsList
from .models import TblReviewList
from .models import TblIndustryList
from datetime import datetime

def news_list(request) :
	today_date = datetime.today().strftime('%Y-%m-%d')
	used_news_list = TblUsedCarNewsList.objects.all().order_by('-write_date')
	new_news_list = TblNewCarNewsList.objects.all().order_by('-write_date')
	review_list = TblReviewList.objects.all().order_by('-write_date')
	industry_list = TblIndustryList.objects.all().order_by('-write_date')
	return render(request, 'website/news_list.html', {'used_news_list': used_news_list, 'today_date': today_date, 'new_news_list': new_news_list, 'review_list': review_list, 'industry_list': industry_list})