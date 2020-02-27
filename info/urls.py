from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    # /info/        (student list)
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /register/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /info/41/     (student detail page)
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]