from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path("fruits_show/<int:id>/",views.fruits_show, name="fruits_show"),
    
    path('Reorder/',views.Reorder,name='Reorder'),
    path('buy/<int:id>/',views.buy,name='buy'),
    path('show_buy/',views.show_buy,name='show_buy'),
    path('increase_qty/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease_qty/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:id>/', views.remove, name='remove'),
    path('checkout/', views.checkout, name='checkout'),
    path("order_success/",views.order_success, name="order_success"),
    path("reorder/<int:id>/",views.reorder_items,name="reorder_items"),
    path("settings/",views.settings,name="settings"),
    path("search/", views.search, name="search"),    
    path("profile/", views.profile, name="profile"),

    
    
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('signout/',views.signout,name='signout'),
    path("change-password/", views.change_password, name="change_password"),
    path("delete-account/", views.delete_account, name="delete_account"),
    
    
    
]
