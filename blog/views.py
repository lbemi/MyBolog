from django.shortcuts import render
from blog.models import *
from django.views.generic import ListView,DetailView
from django.db.models import Q
from .forms import CommentForm
from django.http import HttpResponse
import markdown

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


class AritcleDetail(DetailView):
    model = Article
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        comment_form = CommentForm
        content = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(article=self.kwargs['pk'])
        content['comment_list'] = self.comment_sort(comments)
        content['comment_form'] = comment_form
        try:
            content['session'] = {
                'name':self.request.seesion['name'],
                'email':self.request.seesion['email'],
                'content': self.request.seesion['content']
            }
        except:
            pass
        content['article'].content = markdown.markdown(content['article'].content, extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        return content

    def comment_sort(self, comments):
        self.commet_list = []
        self.top_level = []
        self.sub_level = {}
        for comment in comments:
            print(comment.content)
            comment.content = markdown.markdown(comment.content, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
            if comment.reply == None:
                self.top_level.append(comment)
            else:
                self.sub_level.setdefault(comment.reply.id, []).append(comment)
        for top_comment in self.top_level:
            self.format_show(top_comment)
        return self.commet_list

    def format_show(self, top_comment):
        self.commet_list.append(top_comment)
        try:
            self.kids = self.sub_level[top_comment.id]
        except KeyError:
            pass
        else:
            for kid in self.kids:
                self.format_show(kid)

def pub_commet(request):
    if request.method == 'POST':
        request.session['name'] = request.POST.get('name')
        request.session['email'] = request.POST.get('email')
        comment = Comment()
        comment.article = Article.objects.get(id = request.POST.get('article'))
        if request.POST.get('reply') != '0':
            comment.reply = Comment.objects.get(id=request.POST.get('reply'))
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            try:
                form.save()
                result = '200'
                request.session['content'] = ''
            except:
                request.session['content'] = request.POST.get('content')
                result = '100'
        else:
            result = '100'
        return HttpResponse(result)
    else:
        return HttpResponse('非法请求！！！')