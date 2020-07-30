from django.urls import path,include
from .views import *


urlpatterns = [
    path("toComment",toComment,name="toComment"),
    path("getComment",get_comment,name="getComment"),
    path("toComment2", toComment2, name="toComment2"),
    path("getComment2", get_comment2, name="getComment2"),
    path("toComment3", toComment3, name="toComment3"),
    path("getComment3", get_comment3, name="getComment3"),
    path("getComments", get_comments, name="getComments"),
]