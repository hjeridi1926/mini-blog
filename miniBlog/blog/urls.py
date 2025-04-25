from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('register/',views.register.as_view(),name="register"),
    path('login/',views.loginPage.as_view(),name="login"),
    path('listPost/',views.listPost.as_view(),name="listPost"),
    path('editPost/',views.editPost.as_view(),name="editPost"),
    path("deletePost/<int:pk>/",views.deletePost.as_view(),name="deletePost"),
    path('postDetail/<int:pk>/',views.postDetail.as_view(),name="postDetail"),
    path('editComment/<int:npost>/',views.editComment.as_view(),name="editComment"),
    path('deleteComment/<int:pk>/',views.deleteComment.as_view(),name="deleteComment"),
    path('logout/',views.lgoutView.as_view(),name="logout"),
    path('',views.loginPage.as_view(),name="root")
]
