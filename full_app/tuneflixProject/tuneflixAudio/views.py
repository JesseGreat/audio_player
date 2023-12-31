from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
import requests
import base64
from django.conf import settings
import time
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Music, Video
from .serializers import MusicSerializer, VideoSerializer




class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer







# Initialize variables for access token and its expiration timestamp
access_token = None
token_expiration = 0

def refresh_access_token(client_id, client_secret):
    token_refresh_url = 'https://accounts.spotify.com/api/token'
    
    # Prepare the request data for token refresh
    data = {
        'grant_type': 'client_credentials',
    }

    # Create a base64-encoded string of your client ID and client secret
    client_credentials = f'{client_id}:{client_secret}'
    base64_credentials = base64.b64encode(client_credentials.encode()).decode()

    # Set the headers for the request
    headers = {
        'Authorization': f'Basic {base64_credentials}'
    }

    try:
        # Send a POST request to the token refresh URL
        response = requests.post(token_refresh_url, data=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            new_access_token = data.get('access_token')
            # Calculate the token expiration timestamp (current time + 1 hour)
            token_expiration = int(time.time()) + 3600

            return new_access_token
        else:
            # Handle token refresh error
            print(f"Token refresh failed. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exception
        print(f"An error occurred during token refresh: {str(e)}")
        return None

@api_view(['GET'])
def newAlbumRelease(request):
    global access_token
    global token_expiration

    # Your Spotify API credentials (retrieved from settings.py)
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    current_time = int(time.time())  # Get the current timestamp

    # Check if the access token has expired or doesn't exist
    if not access_token or current_time >= token_expiration:
        # Token has expired or is not available, refresh it
        access_token = refresh_access_token(client_id, client_secret)

        if not access_token:
            return JsonResponse({'error': 'Access token refresh failed'}, status=500)

        # Update the token expiration timestamp
        token_expiration = int(time.time()) + 3600

    # Spotify API endpoint for new releases
    base_url = 'https://api.spotify.com/v1'
    new_releases_url = f'{base_url}/browse/new-releases'

    # Set up headers for authorization using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    try:
        # Make a GET request to get new releases
        response = requests.get(new_releases_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Extract the relevant data from the JSON response
            albums = data.get('albums', {}).get('items', [])

            # Return the data as a JSON response
            return JsonResponse({'albums': albums})
        else:
            # Handle error when retrieving data from Spotify
            return JsonResponse({'error': f'Failed to fetch data from Spotify: {response.content.decode()}'}, status=500)
    except requests.exceptions.RequestException as e:
        # Handle request exception
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    


@api_view(['GET'])
def get_artist_top_tracks(request, id):
    global access_token
    global token_expiration

    # Your Spotify API credentials (retrieved from settings.py)
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    current_time = int(time.time())  # Get the current timestamp

    # Check if the access token has expired or doesn't exist
    if not access_token or current_time >= token_expiration:
        # Token has expired or is not available, refresh it
        access_token = refresh_access_token(client_id, client_secret)

        if not access_token:
            return Response({'error': 'Access token refresh failed'}, status=500)

        # Update the token expiration timestamp
        token_expiration = int(time.time()) + 3600

     # Retrieve the "country" query parameter from the request
    country = request.query_params.get('country', 'US')  # Default to 'US' if not provided
    
    # Spotify API endpoint for an artist's top tracks
    base_url = 'https://api.spotify.com/v1'
    artist_top_tracks_url = f'{base_url}/artists/{id}/top-tracks?country={country}'
   
    # Set up headers for authorization using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    try:
        # Make a GET request to get the artist's top tracks
        response = requests.get(artist_top_tracks_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            # Extract the relevant data from the JSON response
            tracks = data.get('tracks', [])

            # Return the data as a DRF Response
            return Response({'tracks': tracks})
        else:
            # Handle error when retrieving data from Spotify
            return Response({'error': f'Failed to fetch data from Spotify: {response.content.decode()}'}, status=500)
    except requests.exceptions.RequestException as e:
        # Handle request exception
        return Response({'error': f'An error occurred: {str(e)}'}, status=500)


@api_view(['GET'])
def get_available_genre_seeds(request):
    global access_token
    global token_expiration

    # Your Spotify API credentials (retrieved from settings.py)
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    current_time = int(time.time())  # Get the current timestamp

    # Check if the access token has expired or doesn't exist
    if not access_token or current_time >= token_expiration:
        # Token has expired or is not available, refresh it
        access_token = refresh_access_token(client_id, client_secret)

        if not access_token:
            return Response({'error': 'Access token refresh failed'}, status=500)

        # Update the token expiration timestamp
        token_expiration = int(time.time()) + 3600

    # Spotify API endpoint for available genre seeds
    base_url = 'https://api.spotify.com/v1'
    genre_seeds_url = f'{base_url}/recommendations/available-genre-seeds'

    # Set up headers for authorization using the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    try:
        # Make a GET request to get available genre seeds
        response = requests.get(genre_seeds_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            genre_seeds = data.get('genres', [])

            # Return the available genre seeds as a DRF Response
            return Response(genre_seeds)
        else:
            # Handle error when retrieving data from Spotify
            return Response({'error': f'Failed to fetch genre seeds from Spotify: {response.content.decode()}'}, status=500)
    except requests.exceptions.RequestException as e:
        # Handle request exception
        return Response({'error': f'An error occurred: {str(e)}'}, status=500)
    