#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import urllib.request
import os
import re
import pyqrcode

DEVELOPER_KEY = open('api.key').read().strip()

def get_thumbnails():
  youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

  playlist_items = []
  next_page_token = None
  while True:
    response = youtube.playlistItems().list(
      part='snippet,contentDetails',
      playlistId='PLtLUb68F1KiPYTU3LWhq-YxRGkNdBCmI1',
      maxResults=50,
      pageToken=next_page_token,
    ).execute()
    playlist_items = playlist_items + response['items']
    try:
      next_page_token = response['nextPageToken']
    except KeyError:
      break

  for item in playlist_items:
    title = item['snippet']['title']
    video_id = item['contentDetails']['videoId']
    thumbnails = item['snippet']['thumbnails']

    best_thumbnail = max(thumbnails.values(), key=lambda item: item['width'])
    ascii_title = title.encode('ascii', 'ignore').decode()
    ascii_title = re.sub(r'[/:]', '', ascii_title)
    os.mkdir(ascii_title)
    urllib.request.urlretrieve(best_thumbnail['url'], '%s/thumbnail.jpg' % ascii_title)
    url = pyqrcode.create('https://youtu.be/%s' % video_id)
    url.svg('%s/qr.svg', scale=8)
    print('%s %s' % (title, video_id))


if __name__ == "__main__":
  try:
    get_thumbnails()
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    #import pdb;pdb.set_trace()
