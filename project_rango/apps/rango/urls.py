from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.default, name='rango_default'),
    url(r'^about/', views.about, name='rango_about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_slug>[\w\-]+)/$', views.category_detail, name='category_detail'),
    url(r'^category/(?P<category_slug>[\w\-]+)/add_page/$', views.add_page, name='rango_add_page'),
    url(r'^register/$', views.register, name='rango_register'),
    url(r'^login/$', views.user_login, name='rango_login'),
    url(r'^logout/$', views.user_logout, name='rango_logout'),
    url(r'^restricted/$', views.restricted, name='rango_restricted'),
]