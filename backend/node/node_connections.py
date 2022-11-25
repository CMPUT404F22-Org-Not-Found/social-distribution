"""Contains the functions that connect to other nodes."""

import requests

from .models import Node
from author.models import Author
from author.serializers import AuthorSerializer

import logging
logger = logging.getLogger(__name__)

def update_db_with_global_authors():
    """Update the database with authors from other nodes."""
    logger.error("Updating database with global authors")
    try:
        for node in Node.objects.filter(is_connected=True):
            authors_url = f"{node.host}authors/"
            response = requests.get(authors_url, auth=(node.username, node.password))
            if response.status_code == 200:
                authors = AuthorSerializer(data=response.json()["items"], many=True)
                if authors.is_valid():
                    authors.save()
                else:
                    logger.error(authors.errors)
    except Exception as e:
        logger.error(e)
