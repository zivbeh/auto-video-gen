# This code is a Python script for uploading a video to YouTube using the YouTube Data API.
# It defines functions for
# handling authentication,
# initializing the upload,
# and implementing resumable uploads.

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Define valid privacy statuses for uploaded videos
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# Function to get an authenticated service for accessing YouTube API
def get_authenticated_service():
    # Create an OAuth flow from client secrets file
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)
    # Create or load credentials and authorize the HTTP client
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    # Build and return the YouTube API service
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))

# Function to initialize the video upload
def initialize_upload(youtube, args):
    tags = None
    if args["keywords"]:
        tags = args["keywords"].split(",")

    # Create a dictionary representing the video metadata and status
    body = dict(
        snippet=dict(
            title=args["title"],
            description=args["description"],
            tags=tags,
            categoryId=args["category"] # research about this one -------
        ),
        status=dict(
            privacyStatus=args["privacyStatus"]
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(   
        part=",".join(body.keys()),
        body=body,
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request.
        media_body=MediaFileUpload(args["file"], chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)


# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")  # Print a message to indicate the upload is in progress
            status, response = insert_request.next_chunk()  # Attempt to upload the next chunk of the video

            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])  # If a video ID is present in the response, the upload was successful
                else:
                    exit("The upload failed with an unexpected response: %s" % response)  # If there is no video ID, exit the program with an error message

        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)  # Handle retriable HTTP errors
            else:
                raise  # Raise other HTTP errors

        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e  # Handle other retriable errors

        if error is not None:
            print(error)  # Print the error message
            retry += 1  # Increment the retry counter
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")  # If the maximum number of retries is exceeded, exit the program

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)  # Sleep for a random duration and then retry
            time.sleep(sleep_seconds)


if __name__ == '__main__':
    # Define video upload parameters
    args = {
        "file": "/Users/zivbe/Documents/automatic-video-gen/src/output.mp4",
        "title": "California",
        "description": "Had fun surfing in Santa Cruz",
        "keywords": "surfing,Santa Cruz",
        "category": "22",
        "privacyStatus": "private"
    }

    # Check if the specified file exists
    if not os.path.exists(args["file"]):
        exit("Please specify a valid file.")  # If the file does not exist, exit with an error message

    # Get an authenticated YouTube service
    youtube = get_authenticated_service()

    try:
        # Initialize the video upload
        initialize_upload(youtube, args)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

