"""Contains the functions that connect to other nodes."""

import requests
import logging

from .models import Node
from author.models import Author
from author.serializers import AuthorSerializer
from post.models import Post
from post.serializers import PostSerializer
from inbox.models import Inbox

logger = logging.getLogger(__name__)

LOCAL_HOST_NAMES = ["http://127.0.0.1/", "https://cmput404-t04.herokuapp.com/"]

def update_db_with_global_authors():
    """Update the database with authors from other nodes."""
    try:
        for node in Node.objects.filter(is_connected=True):
            logger.error(f"Attempting to update authors from node {node.host}")
            authors_url = f"{node.host}authors/"
            response = requests.get(authors_url, auth=(node.username, node.password))
            if response.status_code == 200:
                authors = AuthorSerializer(data=response.json()["items"], many=True)
                if authors.is_valid():
                    authors.save()
                else:
                    logger.error(f"Could not save authors from {node.host}, {authors.errors}")
            else:
                logger.error(f"Could not get authors from {node.host}, {response.status_code} - {response.reason}")
    except Exception as e:
        logger.error(e)


def send_post_to_inboxes(post: Post, author: Author, only_to_followers: bool = False) -> None:
    """Send a post to all inboxes. If local author add to inbox, else post to global author inbox."""
    authors_to_send_to = []
    if only_to_followers:
        authors_to_send_to = list(author.followers.all())
    else:
        authors_to_send_to = list(Author.objects.all())
    
    for author_to_send_to in authors_to_send_to:
        if is_local_author(author_to_send_to):
            logger.error(f"Attempting to send post to local author {author_to_send_to.url, author_to_send_to.displayName}")
            inbox = Inbox.objects.get(author=author_to_send_to)
            inbox.posts.add(post)
        else:
            logger.error(f"Attempting to send post to global author {author_to_send_to.url, author_to_send_to.displayName}")
            send_post_to_global_inbox(post, author_to_send_to)


def send_post_to_global_inbox(post: Post, author: Author) -> None:
    """Send a post to a global author's inbox."""
    try:
        node = Node.objects.get(host=author.host)
    except:
        logger.error(f"Could not find node for author {author.url, author.displayName}")
        return

    if not node.is_connected:
        return

    post_url = f"{author.url}/inbox/"
    post_data = PostSerializer(post).data
    post_data.pop("commentsSrc")
    response = requests.post(post_url, json=post_data, auth=(node.username, node.password))
    if response.status_code != 200:
        logger.error(response.reason)
    logger.error(f"Sent post to global inbox {node.host}")


def is_local_author(author: Author) -> bool:
    """Return true if the author is local."""
    return author.host in LOCAL_HOST_NAMES
