"""
URL configuration for tuneflixProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tuneflixAudio import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi





schema_view = get_schema_view(
    openapi.Info(
        title="tuneFlix",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tuneflixProject/', include('tuneflixAudio.urls')),
    # path('music/', views.MusicViewSet.as_view(), name='music-list'),
    # path('videos/', views.VideoViewSet.as_view(), name='video-List'),
    path('new-release/', views.newAlbumRelease, name='new-release'),
    path('artist/<str:id>/top-tracks/', views.get_artist_top_tracks, name='get_artist_top_tracks'),
    path('get-available-genre-seeds/', views.get_available_genre_seeds, name='get_available_genre_seeds'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
]
