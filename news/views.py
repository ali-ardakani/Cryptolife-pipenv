from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from datetime import datetime , timedelta
import re
from accounts.models import CustomUser
import requests
from GoogleNews import GoogleNews
from .models import Comment, News, Category
from .forms import NewsForm, CommentForm


def LikeView(request, pk):
    news = get_object_or_404(News, id=request.POST.get('news_id'))
    liked = False
    if news.like_news.filter(id=request.user.id).exists():
        news.like_news.remove(request.user)
        liked = False
    elif news.unlike_news.filter(id=request.user.id).exists():
        news.unlike_news.remove(request.user)
        news.like_news.add(request.user)
        unliked = False
    else:
        news.like_news.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))

def UnLikeView(request, pk):
    news = get_object_or_404(News, id=request.POST.get('news_id'))
    unliked = False
    if news.unlike_news.filter(id=request.user.id).exists():
        news.unlike_news.remove(request.user)
        unliked = False
    elif news.like_news.filter(id=request.user.id).exists():
        news.like_news.remove(request.user)
        news.unlike_news.add(request.user)
        liked = False
    else:
        news.unlike_news.add(request.user)
        unliked = True
    
    return HttpResponseRedirect(reverse('news_detail', args=[str(pk)]))
    

def CommentLikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    liked = False
    if comment.like_comment.filter(id=request.user.id).exists():
        comment.like_comment.remove(request.user)
        liked = False
    elif comment.unlike_comment.filter(id=request.user.id).exists():
        comment.unlike_comment.remove(request.user)
        comment.like_comment.add(request.user)
        unliked = False
    else:
        comment.like_comment.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('news_detail', args=[str(comment.news.id)]))

def CommentUnLikeView(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    unliked = False
    if comment.unlike_comment.filter(id=request.user.id).exists():
        comment.unlike_comment.remove(request.user)
        unliked = False
    elif comment.like_comment.filter(id=request.user.id).exists():
        comment.like_comment.remove(request.user)
        comment.unlike_comment.add(request.user)
        liked = False
    else:
        comment.unlike_comment.add(request.user)
        unliked = True
    
    return HttpResponseRedirect(reverse('news_detail', args=[str(comment.news.id)]))

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    def get_context_data(self, *args, **kwargs):
        context = super(NewsListView, self).get_context_data(**kwargs)
        def google_news(name):
            googlenews = GoogleNews()
            googlenews = GoogleNews(lang='en')
            googlenews = GoogleNews(period='1d')
            googlenews.get_news(name+ ' ')
            googlenews = googlenews.results()[0:5]

            return googlenews

        googlenews = google_news('cryptocurrency') + google_news('bitcoin')
        for news in googlenews:
            if news['datetime'] == None:

                if 'minutes' in news['date']:
                    minutes = int(float(re.sub(r"\s.*", '', news['date'])))
                    news['datetime'] = datetime.now() - timedelta(minutes=minutes)
                
                if 'seconds' in news['date']:
                    seconds = int(float(re.sub(r"\s.*", '', news['date'])))
                    news['datetime'] = datetime.now() - timedelta(seconds=seconds)

        news_obj = News.objects.all().values()
        for news in news_obj:
            news_dict = {}
            news_dict['pk'] = news['id']
            news_dict['title'] = news['title']
            news_dict['site'] = str(CustomUser.objects.get(id = news['author_id']))
            news_dict['datetime'] = news['datetime'].replace(tzinfo=None)
            news_dict['desc'] = news['body']
            news_dict['img'] = news['header_image']
            date = datetime.now() - news_dict['datetime']
            hours, remainder = divmod(date.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours != 0:
                news_dict['date'] = str(int(hours)) + ' ' + 'hours ago'
            elif minutes != 0:
                news_dict['date'] = str(int(minutes)) + ' ' + 'minutes ago'
            else:
                news_dict['date'] = str(int(seconds)) + ' ' + 'seconds ago'

            googlenews.append(news_dict)

        result = []
        result_title_list = []
        for news in googlenews:
            news_title = list(news.values())[0]
            if news_title not in result_title_list:
                if 'pk' in news.keys():
                    result.append(news)
                else:
                    result_title_list.append(news_title)
                    result.append(news)

        result = sorted(result, key = lambda i: i['datetime'], reverse=True)
        
        context['news_cryptocurrency'] = result

        return context



def CategoryView(request, slug):
    try:
        category_news = News.objects.filter(category=Category.objects.get(slug=slug.replace('-', ' ')))
        return render(request, 'news/categories.html', {'slug':slug.title().replace('-', ' '), 'category_news':category_news})
    except:
        return render(request, '404.html')
        
class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(News, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_unlikes = stuff.total_unlikes()
        liked = False
        if stuff.like_news.filter(id =self.request.user.id).exists():
            liked = True
        unliked = False
        if stuff.unlike_news.filter(id =self.request.user.id).exists():
            unliked = True
        context["total_likes"] = total_likes
        context["total_unlikes"] = total_unlikes
        context["liked"] = liked
        context["unliked"] = unliked
        getobjector404 = True
        try:
            stuff_comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        except:
            getobjector404 = False
        if getobjector404 == True:
            stuff_comment = get_object_or_404(Comment, id=self.kwargs['pk'])
            total_likes_comment = stuff_comment.total_likes_comment()
            total_unlikes_comment = stuff_comment.total_unlikes_comment()
            liked_comment = False
            if stuff_comment.like_comment.filter(id =self.request.user.id).exists():
                liked_comment = True
            unliked_comment = False
            if stuff_comment.unlike_comment.filter(id =self.request.user.id).exists():
                unliked_comment = True
            context["total_likes_comment"] = total_likes_comment
            context["total_unlikes_comment"] = total_unlikes_comment
            context["liked_comment"] = liked_comment
            context["unliked_comment"] = unliked_comment

        return context



class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_edit.html'

    def get_success_url(self):
        return reverse_lazy('news_detail', args=[str(self.object.id)])

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('news.all') or self.request.user.has_perm('news.change_news') or obj.author == self.request.user:
            return True 


class NewsCommentsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ('comment',)
    template_name = 'news/comment_edit.html'

    def get_absolute_url(self):
        return reverse_lazy('news_detail', args=[str(self.object.news.id)])

    def get_object(self, *__, **___):
        return Comment.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('news.all') or self.request.user.has_perm('news.delete_news') or obj.author == self.request.user:
            return True 



class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('news.all') or self.request.user.has_perm('news.delete_news') or obj.author == self.request.user:
            return True 


class NewsCommentsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'news/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('news_detail', args=[str(self.object.news.id)])

    def form_valid(self, form):
        form.instance.news_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('news.all') or self.request.user.has_perm('news.delete_news') or obj.author == self.request.user:
            return True 



class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news_new.html'
    permission_required = 'news.add_news'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryCreatingView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'news/category_new.html'
    permission_required = 'news.add_news'
    fields = '__all__'


class NewsCommentsCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'news/comment_news_new.html'
    form_class = CommentForm


    def form_valid(self, form):
        form.instance.news_id = self.kwargs['pk_news']
        form.instance.author = self.request.user
        return super().form_valid(form)



def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)


# def prices_list(request):

#     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     parameters = {
#     'start':'1',
#     'limit':'5000',
#     'convert':'USD'
#     }

#     headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': 'c1f53ff1-4bdc-4db1-993e-1e7e5994a29c',
#     }

#     session = Session()
#     session.headers.update(headers)

#     try:
#         response = session.get(url, params=parameters)
#         data = json.loads(response.text)
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)

#     data = data['data']
#     name_list = []
#     for coin in data:
#         name_list.append(coin['name'])

#     zip_data = zip(name_list, data)
#     dict_data = dict(zip_data)


#     return render(request, 'price/prices_list.html', {'dict_data' : dict_data})


# def prices_list(request):
#     url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
#     data = requests.get(url).json()
#     context = {'data': data}

#     return render(request, 'price/prices_list.html', context)



def get_coins_markets(request, page, **kwargs):
    """List all supported coins price, market cap, volume, and market related data"""
    context = {}
    url = 'https://api.coingecko.com/api/v3/'
    kwargs['vs_currency'] = 'usd'

    api_url = '{0}coins/markets'.format(url)
    api_url = '{0}?vs_currency=usd&order=market_cap_desc&per_page=100&page={1}&sparkline=false'.format(api_url, page)

    data = requests.get(api_url).json()
    for coin in data:
        coin['current_price'] = currency(coin['current_price'])
        coin['market_cap'] = currency(coin['market_cap'])
        coin['total_volume'] = currency(coin['total_volume'])
        coin['circulating_supply'] = re.sub('\$', '', currency(coin['circulating_supply']))
    context['data'] = data
    context['page'] = page

    return render(request, 'price/prices_list.html', context)


# def price_detail(requset, slug):
#     website = requests.get('https://coinmarketcap.com/currencies/%s/' % slug)
#     soup = BeautifulSoup(website.text, 'html.parser')
#     price_usd = soup.find('div', {"class":"priceValue___11gHJ"})
#     price_usd = price_usd.text
#     market_cap = soup.find('div', {"class":"statsValue___2iaoZ"})
#     market_cap = market_cap.text
#     return render(requset, 'price/price_detail.html', {'price_usd' : price_usd, 'market_cap' : market_cap})

def currency(volume):
            if int(float(volume)) > 0 or int(float(volume)) < 0:
                if int(float(volume)) > 10000 or int(float(volume)) < -10000:
                    volume = float(volume)
                    price = "%.2f" % volume
                    profile = re.compile(r"(\d)(\d\d\d[.,])")
                    while 1:
                        price, count = re.subn(profile,r"\1,\2",price)
                        if not count: 
                            price = re.sub(r"\.\d*", '', price)
                            price = '$' + price
                            break
                    return price
                else:
                    volume = float(volume)
                    price = "%.2f" % volume
                    profile = re.compile(r"(\d)(\d\d\d[.,])")
                    while 1:
                        price, count = re.subn(profile,r"\1,\2",price)
                        if not count: 
                            price = '$' + price
                            break
                    return price
            
            else:
                volume = '$' + str(volume)
                return volume

def get_coin_by_id(request,id, **kwargs):
        """Get current data (name, price, market, ... including exchange tickers) for a coin"""

        context = {}

        url = 'https://api.coingecko.com/api/v3/'
        kwargs['vs_currency'] = 'usd'

        api_url = '{0}coins/{1}/'.format(url, id)
        
        data = requests.get(api_url).json()


        data['Volume_Market_Cap'] = '%.5f' % (float(data['market_data']['total_volume']['usd']) / float(data['market_data']['market_cap']['usd']))
        data['market_data']['current_price']['usd'] = currency(data['market_data']['current_price']['usd'])
        # This variable is created for comparison in the template. 
        data['market_data']['price_change_percentage_24h_if'] = float(data['market_data']['price_change_percentage_24h'])
        data['market_data']['price_change_percentage_24h'] = '%.2f' % data['market_data']['price_change_percentage_24h']
        data['market_data']['market_cap_change_percentage_24h_if'] = float(data['market_data']['market_cap_change_percentage_24h'])
        data['market_data']['market_cap_change_percentage_24h'] = '%.2f' % data['market_data']['market_cap_change_percentage_24h']
        data['market_data']['price_change_24h'] = currency(data['market_data']['price_change_24h'])
        data['market_data']['low_24h']['usd'] = currency(data['market_data']['low_24h']['usd'])
        data['market_data']['high_24h']['usd'] = currency(data['market_data']['high_24h']['usd'])
        data['market_data']['total_volume']['usd'] = currency(data['market_data']['total_volume']['usd'])
        data['market_data']['market_cap']['usd'] = currency(data['market_data']['market_cap']['usd'])
        if data['market_data']['fully_diluted_valuation'] != {}:
            data['market_data']['fully_diluted_valuation']['usd'] = currency(data['market_data']['fully_diluted_valuation']['usd'])
        else:
            data['market_data']['fully_diluted_valuation'] = False
        data['market_data']['market_cap_change_24h'] = currency(data['market_data']['market_cap_change_24h'])
        data['market_data']['circulating_supply'] = re.sub('\$', '', currency(data['market_data']['circulating_supply']))
        if data['market_data']['total_supply'] != None:
            data['market_data']['total_supply'] = re.sub('\$', '', currency(data['market_data']['total_supply']))
        else:
            data['market_data']['total_supply'] != False
        if data['market_data']['max_supply'] != None:
            data['market_data']['max_supply'] = re.sub('\$', '', currency(data['market_data']['max_supply']))
        else:
            data['market_data']['max_supply'] = False
        

        if data['links']['homepage'].count('') == 3:
            data['links'].pop('homepage')
            
        if data['links']['blockchain_site'].count('') == 3:
            data['links'].pop('blockchain_site')
            
        if data['links']['official_forum_url'].count('') == 3:
            data['links'].pop('official_forum_url')
            
        if data['links']['chat_url'].count('') == 3:
            data['links'].pop('chat_url')
            
        if data['links']['announcement_url'].count('') == 2:
            data['links'].pop('announcement_url')



        url_companies = "https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin"

        companies = requests.get(url_companies).json()

        for company in companies['companies']:
            company['total_holdings'] = re.sub('\$', '', currency(company['total_holdings']))
            company['total_entry_value_usd'] = currency(company['total_entry_value_usd'])
            company['total_current_value_usd'] = currency(company['total_current_value_usd'])

        context['companies'] = companies            

        context['data'] = data
        if data['market_data']['market_cap_rank'] <= 15:
            googlenews = GoogleNews()
            googlenews = GoogleNews(lang='en')
            googlenews = GoogleNews(period='1d')
            googlenews.get_news(data['name'])
            googlenews = googlenews.results()[:10]
        else:
            googlenews = GoogleNews()
            googlenews = GoogleNews(lang='en')
            googlenews = GoogleNews(period='1d')
            googlenews.get_news(data['name'] + ' ' + 'crypto')
            googlenews = googlenews.results()[:10]
        
        for news in googlenews:
            if 'minutes' in news['date']:
                    minutes = int(float(re.sub(r"\s.*", '', news['date'])))
                    news['datetime'] = datetime.now() - timedelta(minutes=minutes)
                
            if 'seconds' in news['date']:
                seconds = int(float(re.sub(r"\s.*", '', news['date'])))
                news['datetime'] = datetime.now() - timedelta(seconds=seconds)


        category = Category.objects.get(slug=data['name'].lower())
        news_obj = News.objects.filter(category=category).values()
        for news in news_obj:
            news_dict = {}
            news_dict['pk'] = news['id']
            news_dict['title'] = news['title']
            news_dict['site'] = str(CustomUser.objects.get(id = news['author_id']))
            news_dict['datetime'] = news['datetime'].replace(tzinfo=None)
            news_dict['desc'] = news['body']
            news_dict['category'] = data['name'].lower()
            news_dict['img'] = news['header_image']
            date = datetime.now() - news_dict['datetime']
            hours, remainder = divmod(date.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours != 0:
                news_dict['date'] = str(int(hours)) + ' ' + 'hours ago'
            elif minutes != 0:
                news_dict['date'] = str(int(minutes)) + ' ' + 'minutes ago'
            else:
                news_dict['date'] = str(int(seconds)) + ' ' + 'seconds ago'

            googlenews.append(news_dict)

        googlenews = sorted(googlenews, key = lambda i: i['datetime'], reverse=True)

        context['googlenews'] = googlenews

        

        return render(request, 'price/price_detail.html', context)


# def google_news(request):

#     context = {}
#     name = request.POST.get('name_coin')
#     googlenews = GoogleNews()
#     googlenews = GoogleNews(lang='en')
#     googlenews = GoogleNews(period='1d')
#     googlenews.get_news(name)
#     googlenews = googlenews.results()[0:5]
    
#     for news in googlenews:
#         queryset = Google_News.objects.create(
#             title = news['title'],
#             site = news['site'],
#             description = news['desc'],
#             date_time = news['datetime'],
#             image = news['img'],
#         )
#         queryset.category.set(Category.objects.filter(slug=name))
#         queryset.save()

#     return HttpResponseRedirect(reverse('news_list'))
    




    




