from googleapiclient.discovery import build
from create_helper import credentials
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
YOUTUBE_API_SERVICE_NAME = 'youtube'
DEVELOPER_KEY = credentials.DEVELOPER_KEY
YOUTUBE_API_VERSION = 'v3'

def youtube_search(keywords):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=keywords,
    part='snippet',
    maxResults=1
  ).execute()

  videos = ''

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos = search_result['id']['videoId']

  print(videos)

  return videos