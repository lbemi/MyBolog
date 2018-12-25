from django.urls import path, include
from blog import views
urlpatterns = [
    path('', views.index.as_view()),
    path('category/<int:category>',views.CategoryList.as_view(), name ='category'),
    path('search/',views.Search.as_view(), name='search'),
    path('detail/', views.AritcleDetail.as_view(), name= 'detail'),
]