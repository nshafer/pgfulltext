from django.conf.urls import url

from blog import views


urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name="posts"),
]
