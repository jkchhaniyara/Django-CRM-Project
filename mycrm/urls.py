from django.urls import path
from mycrm import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_user, name="register"),
    path("record/<int:pk>/", views.customer_record, name="record"),
    path("update_record/<int:pk>/", views.update_record, name="update_record"),
    path("add_record/", views.add_record_view, name="add_record"),
    path("record_list/", views.record_list_view, name="record_list"),
    path("fetch_data/", views.fetch_data, name="fetch_data"),
    path(
        "customer_record_ajax/<int:pk>/",
        views.customer_record_ajax,
        name="customer_record_ajax",
    ),
    path(
        "delete_record/<int:pk>/",
        views.delete_record,
        name="delete_record",
    ),
    path("login/", views.login_view, name="login")
    #    path("update_record_ajax/<int:pk>/", views.update_record_ajax, name="update_record_ajax"),
]
