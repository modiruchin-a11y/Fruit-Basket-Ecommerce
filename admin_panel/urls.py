from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_log"),
    path("dashboard/", views.dashboard, name="admin_dashboard"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("categories/", views.categories, name="categories"),
    path("categories/", views.categories, name="add_categories"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/edit/<int:id>/", views.edit_category, name="edit_category"),
    path("categories/delete/<int:id>/", views.delete_category, name="delete_category"),
    path("products/", views.products, name="products"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:id>/", views.edit_product, name="edit_product"),
    path("products/delete/<int:id>/", views.delete_product, name="delete_product"),
    path("orders/", views.orders, name="orders"),
    path("orders/<int:id>/",views.order_details,name="order_details"),
    path("users/",views.users,name="users")
    
]