from django.shortcuts import render
from blog.models import *
from django.views.generic import ListView,DetailView
from django.db.models import Q
from .forms import CommentForm
# Create your views here.

class index(ListView):
    model = Article
    template_name = 'index.html'
    queryset_name = Article.objects.all().order_by('-id')
    paginate_by = 5


class CategoryList(ListView):
    model = Article
    template_name = 'category.html'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(category=self.kwargs['category']).order_by('-id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category'])
        print(category.name)
        context['category'] = category.name
        print('----------------------')
        return context

class Search(ListView):
    model = Article
    template_name = 'search.html'
    paginate_by = 5

    def get_queryset(self):
        key = self.request.GET['key']
        if key:
            return Article.objects.filter(Q(title__icontains=key)|Q(content__icontains=key)).order_by('-id')
        else:
            return None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.GET['key']
        return context

def comment_sort(self,comments):
    self.commet_list = []
    self.top_level = []
    self.sub_level = {}
    for comment in comments:
        if comment.reply == None:
            self.top_level.append(comment)
        else:
            self.sub_level.setdefault(comment.reply.id,[]).append(comment)

def format_show(self,top_comment):
    self.comment_lsit.append(top_comment)
    try:
        self.kids = self.sub_level[top_comment.id]
    except KeyError:
        pass
    else:
        for kid in self.kids:
            self.format_show(kid)
class AritcleDetail(DetailView):
    model = Article
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        comment_form = CommentForm
        content = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(article=self.kwargs['pk'])
        content['commetn_list'] = comment_sort(comments)
        content['comment_form'] = comment_form
        return content


