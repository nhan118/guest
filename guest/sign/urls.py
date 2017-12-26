from django.conf.urls import url
from sign import views_if, views_if_sec


urlpatterns = [
    # sign system interface:
    # ex : /api/add_event/
    url(r'^sec_add_event/', views_if_sec.add_event, name = 'add_event'),
    # ex : /api/add_guest/
    url(r'^sec_add_guest/', views_if_sec.add_guest, name = 'add_guest'),
    # ex : /get_event_list/
    url(r'^sec_get_event_list/', views_if_sec.get_event_list, name = 'get_event_list'),
    # ex : /get_guest_list/
    url(r'^sec_get_guest_list/', views_if_sec.get_guest_list, name = 'get_guest_list'),
    # ex : /guest_sign/
    # url(r'^sec_guest_sign/', views_if_sec.guest_sign, name = "guest_sign"),
    url(r'^user_sign/', views_if.user_sign, name="user_sign"),
 ]