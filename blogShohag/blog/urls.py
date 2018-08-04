from django.urls import path
from django.views.generic.base import RedirectView


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<name>/', views.getAuthor, name='author'),
    path('article/<int:id>/', views.getSingle, name='single_post'),
    path('category/<name>/', views.getTopic, name='topic'),
    path('login/', views.getLogin, name='login'),
    path('logout/', views.getLogout, name='logout'),
    path('create/', views.getCreated, name='create'),
    path('profile/', views.getProfile, name='profile'),
    path('update/<int:post_id>/', views.getUpdate, name='update'),
    path('delete/<int:deleted_post_id>/', views.getDelete, name='delete'),
    path('register/', views.getRegister, name='register'),
    path('create_category/', views.getCreatedCategory, name='create_category'),
    path('category_list/', views.getCategoryList, name='category_list'),
    #path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon/favicon.ico')),

]

