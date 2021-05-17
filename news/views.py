from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .models import Comment, News
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


