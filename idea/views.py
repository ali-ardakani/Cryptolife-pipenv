from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Idea, CommentIdea
from .forms import IdeaForm, CommentIdeaForm
from datetime import datetime
from accounts.models import CustomUser
import json

class IdeaListView(ListView):
    model = Idea
    template_name = 'idea/idea_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaListView, self).get_context_data()
        idea_obj = Idea.objects.all().values()
        for idea in idea_obj:
            idea['datetime'] = idea['datetime'].replace(tzinfo=None)
            date = datetime.now() - idea['datetime']
            hours, remainder = divmod(date.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours != 0:
                idea['date'] = str(int(hours)) + ' ' + 'hours ago'
            elif minutes != 0:
                idea['date'] = str(int(minutes)) + ' ' + 'minutes ago'
            else:
                idea['date'] = str(int(seconds)) + ' ' + 'seconds ago'

            idea['author'] = CustomUser.objects.get(id = idea['author_id'])

        context['ideas'] = idea_obj
            
        return context


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea/idea_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IdeaDetailView, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Idea, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        total_unlikes = stuff.total_unlikes()
        liked = False
        if stuff.like_idea.filter(id =self.request.user.id).exists():
            liked = True
        unliked = False
        if stuff.unlike_idea.filter(id =self.request.user.id).exists():
            unliked = True
        context["total_likes"] = total_likes
        context["total_unlikes"] = total_unlikes
        context["liked"] = liked
        context["unliked"] = unliked
        getobjector404 = True
        try:
            stuff_comment = get_object_or_404(CommentIdea, id=self.kwargs['pk'])
        except:
            getobjector404 = False
        if getobjector404 == True:
            stuff_comment = get_object_or_404(CommentIdea, id=self.kwargs['pk'])
            total_likes_comment = stuff_comment.total_likes_comment()
            total_unlikes_comment = stuff_comment.total_unlikes_comment()
            liked_comment = False
            if stuff_comment.like_comment_idea.filter(id =self.request.user.id).exists():
                liked_comment = True
            unliked_comment = False
            if stuff_comment.unlike_comment_idea.filter(id =self.request.user.id).exists():
                unliked_comment = True
            context["total_likes_comment"] = total_likes_comment
            context["total_unlikes_comment"] = total_unlikes_comment
            context["liked_comment"] = liked_comment
            context["unliked_comment"] = unliked_comment

        return context


def LikeView(request, pk):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    liked = False
    if idea.like_idea.filter(id=request.user.id).exists():
        idea.like_idea.remove(request.user)
        liked = False
    elif idea.unlike_idea.filter(id=request.user.id).exists():
        idea.unlike_idea.remove(request.user)
        idea.like_idea.add(request.user)
        unliked = False
    else:
        idea.like_idea.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('idea:idea_detail', args=[str(pk)]))


def UnLikeView(request, pk):
    idea = get_object_or_404(Idea, id=request.POST.get('idea_id'))
    unliked = False
    if idea.unlike_idea.filter(id=request.user.id).exists():
        idea.unlike_idea.remove(request.user)
        unliked = False
    elif idea.like_idea.filter(id=request.user.id).exists():
        idea.like_idea.remove(request.user)
        idea.unlike_idea.add(request.user)
        liked = False
    else:
        idea.unlike_idea.add(request.user)
        unliked = True
    
    return HttpResponseRedirect(reverse('idea:idea_detail', args=[str(pk)]))


def CommentLikeView(request, pk):
    comment = get_object_or_404(CommentIdea, id=request.POST.get('comment_id'))
    liked = False
    if comment.like_comment_idea.filter(id=request.user.id).exists():
        comment.like_comment_idea.remove(request.user)
        liked = False
    elif comment.unlike_comment_idea.filter(id=request.user.id).exists():
        comment.unlike_comment_idea.remove(request.user)
        comment.like_comment_idea.add(request.user)
        unliked = False
    else:
        comment.like_comment_idea.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('idea:idea_detail', args=[str(comment.idea.id)]))

def CommentUnLikeView(request, pk):
    comment = get_object_or_404(CommentIdea, id=request.POST.get('comment_id'))
    unliked = False
    if comment.unlike_comment_idea.filter(id=request.user.id).exists():
        comment.unlike_comment_idea.remove(request.user)
        unliked = False
    elif comment.like_comment_idea.filter(id=request.user.id).exists():
        comment.like_comment_idea.remove(request.user)
        comment.unlike_comment_idea.add(request.user)
        liked = False
    else:
        comment.unlike_comment_idea.add(request.user)
        unliked = True
    
    return HttpResponseRedirect(reverse('idea:idea_detail', args=[str(comment.idea.id)]))


class IdeaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'idea/idea_edit.html'

    def get_success_url(self):
        return reverse_lazy('idea:idea_detail', args=[str(self.object.id)])

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True 


class IdeaCommentsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CommentIdea
    fields = ('comment_idea',)
    template_name = 'idea/comment_edit.html'

    def get_absolute_url(self):
        return reverse_lazy('idea:idea_detail', args=[str(self.object.idea.id)])

    def get_object(self, *__, **___):
        return CommentIdea.objects.get(pk=self.kwargs['pk'])

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True 



class IdeaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Idea
    template_name = 'idea/idea_delete.html'
    success_url = reverse_lazy('idea:idea_list')

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('idea:idea.all') or self.request.user.has_perm('idea.delete_idea') or obj.author.id == self.request.user.id:
            return True 


class IdeaCommentsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CommentIdea
    template_name = 'idea/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('idea:idea_detail', args=[str(self.object.idea.id)])

    def form_valid(self, form):
        form.instance.idea_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user.has_perm('idea.all') or self.request.user.has_perm('idea.delete_idea') or obj.author == self.request.user:
            return True 



class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    form_class = IdeaForm
    template_name = 'idea/idea_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IdeaCommentsCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    template_name = 'idea/comment_idea_new.html'
    form_class = CommentIdeaForm

    def get_success_url(self):
        return reverse_lazy('idea:idea_detail', args=[str(self.object.idea.id)])


    def form_valid(self, form):
        form.instance.idea_id = self.kwargs['pk_idea']
        form.instance.author = self.request.user
        return super().form_valid(form)

