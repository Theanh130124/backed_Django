from django.urls import path, include
from rest_framework import routers
from courses import views

routers = routers.DefaultRouter()
#Tạo đường dẫn và chỉ view
routers.register('categories',views.CategoryViewSet , basename='categories' )
routers.register('courses',views.CourseViewSet, basename='courses' )
routers.register('lessons' ,views.LessonViewSet , basename='lessons')
routers.register('users', views.UserViewSet , basename='users')
routers.register('comments', views.CommentViewSet , basename='comments')
urlpatterns = [

    path('',include(routers.urls)),
    ]