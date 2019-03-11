from django.conf.urls import include, url
from goods import  views

urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',views.index,name='index'),#首页
]
