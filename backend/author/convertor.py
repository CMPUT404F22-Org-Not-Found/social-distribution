"""Contains the functions neeed to convert the author data format to local format."""

"""One inconsistency between the global and local author data formats is the
    author id field. Whereas in the global format, it is the url e.g.
    "http://127.0.0.1:5454/authors/9de1";
    In the local format, it is the author id is simple the UUID e.g. "9de1".
"""

def convert_author_dict_to_local_format(author_dict: dict) -> dict:
    """Convert the author data format to local format."""
    if "http" in author_dict["id"]:
        author_dict["id"] = author_dict["id"].split("/")[-1]
    return author_dict

def convert_author_dict_to_global_format(author_dict: dict) -> dict:
    """Convert the author data format to global format."""
    author_dict["id"] = f"{author_dict['host']}/authors/{author_dict['id']}"
    return author_dict
