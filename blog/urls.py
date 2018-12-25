from django.urls import path, include
from blog import views
urlpatterns = [
    path('', views.index.as_view()),
    path('category/<int:category>',views.CategoryList.as_view(), name ='category'),
]