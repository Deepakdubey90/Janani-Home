# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-07-30T00:52:11+05:30
# @Email:  tamyworld@gmail.com
# @Filename: urls.py
# @Last modified by:   tushar
# @Last modified time: 2017-08-06T15:18:47+05:30



from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^edit_profile/$', views.update_profile, name='update_profile'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login',
        kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': 'login'}),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^country/states/$', views.StateAjaxView, name='states_of_country'),
]
