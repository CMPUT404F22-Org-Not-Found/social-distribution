# social-distribution

CMPUT 404 Group Project Repo


## Working Endpoints
* Authentication
    1. login/                                                   
        - Login page
    2. logout/                                                 
        - Logout page
    3. register/                                                
        - Register page

* Authors
    1. GET //service/authors/                                   
        - Authors List
    2. GET //service/authors/{AUTHOR_ID}                        
        - Author Profile
    3. POST //service/authors/{AUTHOR_ID}                       
        - Create Author
        
* Post
    1. GET //service/authors/{AUTHOR_ID}/posts/                                   
        - Post List of Author {AUTHOR_ID}
    2. POST //service/authors/{AUTHOR_ID}/posts/                       
        - Creating Post with Random ID 
    3. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}                       
        - Public Post {POST_ID}
    4. POST //service/authors/{AUTHOR_ID}/posts/{POST_ID}
        - Update Post {POST_ID} 
    5. DELETE //service/authors/{AUTHOR_ID}/posts/{POST_ID}
        - Delete Post {POST_ID}
    6. PUT //service/authors/{AUTHOR_ID}/posts/{POST_ID}
        - Create Post {POST_ID}
    7. GET //service/public/
        - Public Post List
        
* Comment
    1. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments              
        - Comment List of the Post {POST_ID}
    2. POST //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments
        - Create comment for Post {POST_ID}
    3. GET //service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}
        - View Comment {COMMENT_ID} of Post {POST_ID}

* Follower
    1. GET //service/author/{AUTHOR_ID}/followers/              
        - Followers List of the the Author
    2. GET //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID} 
        - Check if foreign author is following the Author
    3. POST //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID}
        - Foreign author follows the Author
    4. DELETE //service/author/{AUTHOR_ID}/followers/{FOLLOWER_ID} 
        - Remove foreign author from the Author's followers

* Friend Request
    1. GET //service/author/{AUTHOR_ID}/followers/friendrequest/
        - Pending friend requests recieved by the Author
    2. GET //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID} 
        - Check if foreign author has sent a friend request to the Author
    3. POST //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID}    
        - Foreign author sends a freind request to the Author
    4. DELETE //service/author/{AUTHOR_ID}/followers/friendrequest//{FRIEND_ID}  
        - Remove the friend request sent by the foreign author to the Author

* Likes
    1. GET //service/author/{AUTHOR_ID}/posts/{POST_ID}/likes/  
        - Likes List of the Post
    2. POST //service/author/{AUTHOR_ID}/posts/{POST_ID}/likes/{LIKE_ID} 
        - Author likes the Post, and added to Like DB

* Inbox
    1. GET //service/author/{AUTHOR_ID}/inbox/                  
        - Inbox of the Author, retrieves all the posts, friend requests and likes sent to the author.
    2. POST //service/author/{AUTHOR_ID}/inbox/                 
        - Send a post to the Author's inbox
        - Send a friend request to the author's inbox
        - Send a like to the author's inbox

    Tip: when sending the request for the author dict inside friend request/post, you only
        need to include the author id
