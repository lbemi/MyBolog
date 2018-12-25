from django.shortcuts import render
from blog.models import *
from django.views.generic import ListView

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