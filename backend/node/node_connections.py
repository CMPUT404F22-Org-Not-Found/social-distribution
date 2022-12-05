"""Contains the functions that connect to other nodes."""

import requests
import logging

from .models import Node
from author.models import Author
from author.serializers import AuthorSerializer
from post.models import Post
from post.serializers import PostSerializer
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from like.models import Like
from like.serializers import LikeSerializer
from inbox.models import Inbox
from inbox.request_verifier import verify_author_request, get_author_id_from_url

logger = logging.getLogger(__name__)

LOCAL_HOST_NAMES = ["http://127.0.0.1/", "https://cmput404-t04.herokuapp.com/",
                    "http://127.0.0.1:8000/", "http://testserver/"]

def update_db_with_global_authors():
    """Update the database with authors from other nodes."""
    for node in Node.objects.filter(is_connected=True):
        try:
            logger.error(f"[INFO]: Attempting to update authors from node {node.host}")
            authors_url = f"{node.host}authors/?size=100"
            response = requests.get(authors_url, auth=(node.username, node.password))
            if response.status_code == 200:
                create_or_update_authors(response.json()["items"])
            else:
                logger.error(f"[ERROR]: Could not get authors from {node.host}, {response.status_code} - {response.reason}")
            logger.error(f"[SUCCESS]: Successfully updated authors from node {node.host}")
        except Exception as e:
            logger.error(f"[ERROR]: Exception when getting global authors from {node.host}, {e}")


def create_or_update_authors(author_dicts: list) -> None:
    """Create or update authors from a list of author dicts."""
    try:
        for author_dict in author_dicts:
            author_dict = verify_author_request(author_dict)
            author_id = get_author_id_from_url(author_dict["id"])
            author, created = Author.objects.update_or_create(author_id=author_id, defaults=author_dict)
            if created:
                logger.error(f"[INFO]: Created global author {author.url, author.displayName}")
    except Exception as e:
        logger.error(f"[ERROR]: Exception while creating or updating global authors: {e}")

def send_post_to_inboxes(post: Post, author: Author, only_to_followers: bool = False) -> None:
    """Send a post to all inboxes. If local author add to inbox, else post to global author inbox."""
    authors_to_send_to = []
    if only_to_followers:
        authors_to_send_to = list(author.followers.all())
    else:
        authors_to_send_to = list(Author.objects.all())
    
    for author_to_send_to in authors_to_send_to:
        try:
            if is_local_author(author_to_send_to):
                logger.error(f"[INFO]: Attempting to send post to local author {author_to_send_to.url, author_to_send_to.displayName}")
                inbox, _ = Inbox.objects.get_or_create(author=author_to_send_to)
                inbox.posts.add(post)
            else:
                send_post_to_global_inbox(post, author_to_send_to)
        except Exception as e:
            logger.error(f"[ERROR]: Exception while sending post to {author_to_send_to.url, author_to_send_to.displayName}, {e}")


def send_post_to_global_inbox(post: Post, author: Author) -> None:
    """Send a post to a global author's inbox."""
    logger.error(f"[INFO]: Attempting to send post to global author {author.url, author.displayName}")
    try:
        node = Node.objects.get(host=author.host)
    except:
        logger.error(f"[ERROR]: Could not find node for author {author.url, author.displayName}")
        return

    if not node.is_connected:
        return

    post_url = f"{author.url}/inbox/"
    post_data = PostSerializer(post).data
    post_data.pop("commentsSrc")
    response = requests.post(post_url, json=post_data, auth=(node.username, node.password))

    if response.status_code >= 200:
        logger.error(f"[ERROR]: Could not send post to {author.url}, {response.status_code} - {response.reason}")
    else:
        logger.error(f"[SUCCESS]: Sent post to global inbox {node.host}, {author.url}")


def send_friend_request_to_global_inbox(friend_request: FriendRequest, author: Author) -> None:
    """Send a friend request to a global author's inbox."""
    logger.error(f"[INFO]: Attempting to send friend request to global author {author.url, author.displayName}")
    try:
        node = Node.objects.get(host=author.host)
    except:
        logger.error(f"[ERROR]: Could not find node for author {author.url, author.displayName}")
        return

    if not node.is_connected:
        return

    friend_request_url = f"{author.url}/inbox/"
    friend_request_data = FriendRequestSerializer(friend_request).data
    response = requests.post(friend_request_url, json=friend_request_data, auth=(node.username, node.password))

    if response.status_code >= 400:
        logger.error(f"[ERROR]: Could not send friend request to {author.url}, {response.status_code} - {response.reason}")
    else:
        logger.error(f"[SUCCESS]: Sent friend request to global inbox {node.host}")


def send_like_to_global_inbox(like: Like, author: Author) -> None:
    """Send a like to a global author's inbox."""
    logger.error(f"[INFO]: Attempting to send like to global author {author.url, author.displayName}")
    try:
        node = Node.objects.get(host=author.host)
    except:
        logger.error(f"[ERROR]: Could not find node for author {author.url, author.displayName}")
        return

    if not node.is_connected:
        return

    like_url = f"{author.url}/inbox/"
    like_data = LikeSerializer(like).data
    response = requests.post(like_url, json=like_data, auth=(node.username, node.password))

    if response.status_code >= 400:
        logger.error(f"[ERROR]: Could not send like to {author.url}, {response.status_code} - {response.reason}")
    else:
        logger.error(f"[SUCCESS]: Sent like to global inbox {node.host}")


def is_local_author(author: Author) -> bool:
    """Return true if the author is local."""
    return author.host in LOCAL_HOST_NAMES
