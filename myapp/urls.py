from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('work/',views.work,name='work'),
    path('filter/<int:pk>/',views.filter,name='filter'),
    path('filter_index/<int:pk>/',views.filter_index,name='filter_index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('fpswd/',views.fpswd,name='fpswd'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('change_pswd/',views.change_pswd,name='change_pswd'),

    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),

    path('callback/',views.callback,name='callback'),

    # ==================DASHBORAD=============================
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_charts/',views.admin_charts,name='admin_charts'),
    path('add_services/',views.add_services,name='add_services'),
    path('add_techno/',views.add_techno,name='add_techno'),
    path('add_package/',views.add_package,name='add_package'),

    path('my_packages/',views.my_packages,name='my_packages'),
    path('modify_package/',views.modify_package,name='modify_package'),
    path('delete_package/<int:pk>/',views.delete_package,name='delete_package'),
    path('update_package/<int:pk>/',views.update_package,name='update_package'),

    path('all_techno/',views.all_techno,name='all_techno'),
    path('delete_techno/<int:pk>/',views.delete_techno,name='delete_techno'),
    path('update_techno/<int:pk>/',views.update_techno,name='update_techno'),

    path('blogs/',views.blogs,name='blogs'),
    path('single_blog/<int:pk>/',views.single_blog,name='single_blog'),
    path('my_blogs/',views.my_blogs,name='my_blogs'),

    path('post_comment/<int:pk>/',views.post_comment,name='post_comment'),
    
    path('work_space/',views.work_space,name='work_space'),
    path('search/',views.search,name='search'),

    #=================for AJAX validation============================
    path('ajax/validate/',views.validate,name='validate'),

    #==========================================================
]