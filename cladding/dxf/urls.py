from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('home/',views.home),
    path('lattice/',views.lattice),
    path('home/newjob/',views.new_job),
    path('home/job/<int:id>',views.viewjob),
    path('home/jobhandler/<int:id>',views.job_handler),
    path('home/parthandler/<int:id>',views.part_handler),
    path('download/<str:partid>',views.download_part),
    path('downloadjob/<str:jobid>',views.download_job),
]