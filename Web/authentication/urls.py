from django.conf.urls import url
from . import views

urlpatterns = [
	 # ex : /login
    url(r'^login', views.login, name='login'),
    # ex : /do_login
    url(r'^do_login', views.do_login, name='do_login'),
	 # ex : /do_logout
    url(r'^do_logout', views.do_logout, name='do_logout'),
    # ex : /join
    url(r'^join', views.join, name='join'),
    # ex : /do_join
    url(r'^do_join', views.do_join, name='do_join'),
    # ex : /duplicated
    url(r'^duplicated', views.duplicated, name='duplicated'),
    # ex : /go_board
    url(r'^go_board', views.go_board, name='go_board'),
    # ex : /
    url(r'^', views.main, name='main'),
]
