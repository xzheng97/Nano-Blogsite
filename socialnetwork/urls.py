from django.urls import path
from socialnetwork import views

urlpatterns = [

    path('global_stream', views.global_stream, name='global_stream'),
    path('follower_stream',views.follower_stream, name='follower_stream'),
    path('my_profile',views.my_profile, name='my_profile'),
    path('profile/<int:id>',views.other_profile, name='other_profile'),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('refresh-global', views.refresh_gloabl_json_dumps_serializer),
    path('refresh-follower',views.refresh_follower_json_dumps_serializer),
    # path('get-list-django-serializer', views.get_list_django_serializer),
    # path('get-list-django-serializer', views.get_list_django_serializer),
    path('add-comment', views.add_comment),

]

