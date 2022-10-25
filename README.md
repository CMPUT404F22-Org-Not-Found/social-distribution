# social-distribution

CMPUT 404 Group Project Repo


## Working Endpoints
* Authentication
    1. login/                                                   - Login page
    2. logout/                                                  - Logout page
    3. register/                                                - Register page

* Authors
    1. GET //service/authors/                                   - Authors List
    2. GET //service/authors/{AUTHOR_ID}                        - Author Profile
    3. POST //service/authors/{AUTHOR_ID}                       - Create Author

* Follower
    1. GET //service/author/{AUTHOR_ID}/followers/              - Followers List of the the Author
    2. GET //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID} - Check if foreign author is following the Author
    3. POST //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID}- Foreign author follows the Author
    4. DELETE //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID} - Remove foreign author from the Author's followers

* Friend
    1. GET //service/author/{AUTHOR_ID}/followers/friendrequest/- Pending friend requests recieved by the Author
    2. GET //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID} - Check if foreign author has sent a friend request to the Author
    3. POST //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID}    - Foreign author sends a freind request to the Author
    4. DELETE //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID}  - Remove the friend request sent by the foreign author to the Author
