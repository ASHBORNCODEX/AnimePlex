from django.urls import path
from WebApp import views

urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('single_anime/<int:anime_id>/',views.single_anime,name="single_anime"),
    path('stream_anime/<int:anime_id>/',views.stream_anime,name="stream_anime"),

    path('increment_views/',views.increment_views,name="increment_views"),

    path('sign_in/',views.sign_in,name="sign_in"),
    path('sign_up/',views.sign_up,name="sign_up"),
    path('save_user_reg/',views.save_user_reg,name="save_user_reg"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),

    path('profile_page/',views.profile_page,name="profile_page"),
    path('watch_list/',views.watch_list,name="watch_list"),



    path('remove_anime/<int:Anime_ID>/',views.remove_anime,name="remove_anime"),
    path('filter/<str:filter_type>/<str:filter_value>/', views.filter_anime, name="filter_anime"),



    path('edit_profile_page/',views.edit_profile_page,name="edit_profile_page"),
    path("add_to_watchlist/<int:anime_id>/", views.add_to_watchlist, name="add_to_watchlist"),





]


