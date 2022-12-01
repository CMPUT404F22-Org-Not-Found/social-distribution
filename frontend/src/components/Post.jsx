import { Alert, Avatar, Button, Card, CardActions, CardContent, CardHeader, CardMedia, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, IconButton, ListItem, ListItemText, Snackbar, TextField, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';

import React, { useState, useEffect } from "react"; import './Post.css';
import axios from "axios";
import CreateNewPost from "./CreateNewPost";
import axiosInstance from "../axiosInstance";

var ReactCommonmark = require('react-commonmark');
function Post(props) {
  const {
    id, name, user, author, title, description, contentType, content, img, fromProfile, commentsURL, visibility,
  } = props

  const [openCommentDialog, setOpenCommentDialog] = useState(false);
  const [commentsForPost, setCommentsForPost] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [allLikedObjects, setAllLikedObjects] = useState([]);
  const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const [stateSnackBar, setStateSnackBar] = useState({
    openSnackBar: false,
    vertical: 'top',
    horizontal: 'center',
  });

  const { vertical, horizontal, openSnackBar } = stateSnackBar;

  const handleOpenSnackBar = () => {
    setStateSnackBar({ openSnackBar: true, ...stateSnackBar });
    console.log("Snackbar opened");
  };

  const handleCloseSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setStateSnackBar({ ...stateSnackBar, openSnackBar: false });
    console.log("Snackbar closed");
  };

  // HANDLE COMMENT DIALOG
  const handleClickOpenCommentDialog = () => {
    setOpenCommentDialog(true);
  };

  const handleCloseCommentDialog = () => {
    setOpenCommentDialog(false);
  };

  const handleChangeComment = (event) => {
    setNewComment(event.target.value);
  }

  const getCommentsForPost = () => {
    console.log("CommentsURL:", commentsURL);
    axios.get(commentsURL + "/").then((response) => {
      console.log(response.data.comments);
      setCommentsForPost(response.data.comments);
    });
  }

  const handleSubmitComments = () => {
    const url = "authors/" + authorId;
    axiosInstance.get(url).then((response) => {
      console.log(response);
    })

    const commentDate = new Date();
    const postData = {
      type: "comment",
      author: authorObject,
      comment: newComment,
      contentType: "text/plain",
      published: commentDate.toISOString(),
    };

    axiosInstance.post(commentsURL + "/", postData)
      .then((response) => {
        console.log(response);
        handleCloseCommentDialog();
        handleOpenSnackBar({
          vertical: 'top',
          horizontal: 'center',
        });
      });
    console.log(postData);
    console.log(commentsURL);
    handleCloseCommentDialog();
    handleOpenSnackBar();

    console.log(newComment);
    window.location.reload();
  };

  // HANDLE EDIT DIALOG
  const handleOpenEditDialog = () => {
    setOpenEditDialog(true);
  };

  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
  };

  const handleSubmitEdit = () => {
    const url = author.url + "/posts/" + id + "/";
    const postData = {

    }
  };

  const checkImageExists = (image) => {
    // check if image needs to be displayed
    let style = '';
    if (image === 'null') {
      style = 'none'
    }
    return style;
  }

  const checkFromProfile = () => {
    // check if componenet is being displayed in Profile
    if (fromProfile) {
      return (
        <IconButton aria-label="edit" onClick={handleOpenEditDialog}>
          <EditIcon />
        </IconButton>
      )
    };
  };

  useEffect(() => {
    getCommentsForPost();
    console.log("Comments:", commentsForPost);
    getAllLikedObjects();
    console.log()
    console.log("Liked Objects", allLikedObjects);
  }, []);

  // HANDLE LIKING OBJECTS
  const getAllLikedObjects = () => {
    const url = "/authors/" + authorId + "/liked/"
    axiosInstance.get(url)
      .then((response) => {
        const allLikes = response.data.items;

        const objectIds = []
        for (let i = 0; i < allLikes.length; i++) {
          objectIds.push(allLikes[i].object);
        }
        setAllLikedObjects(objectIds);
      });
  }

  const handleLike = (id, type) => {
    // post a new like to the liked object's author's inbox

    const likeData = {
      author: authorObject,
      type: "like",
      summary: authorObject.displayName + " likes your " + type,
      object: id,
    }

    const objectAuthorID = id.split("/")[4];
    const url = "/authors/" + objectAuthorID + "/inbox/";

    axiosInstance.post(url, likeData)
      .then((response) => {
        console.log(response);
      });
    window.location.reload();

  };

  const displayLike = (id, type) => {
    // check if object has been liked by user, display corresponding icon
    if (allLikedObjects.includes(id)) {
      return (
        <IconButton aria-label="like" style={{ display: checkIfLoggedIn() }}>
          <FavoriteIcon />
        </IconButton>
      );
    } else {
      return (
        <IconButton aria-label="like" onClick={() => handleLike(id, type)} style={{ display: checkIfLoggedIn() }}>
          <FavoriteBorderIcon />
        </IconButton>
      );
    }
  };

  const checkIfLoggedIn = () => {
    // check if token exists, if yes, user is logged in
    const authToken = window.localStorage.getItem("auth-token");
    let style = '';
    if (!authToken) {
      style = 'none'
    }
    return style;
  }

  const checkProfileImage = () => {
    const url = author.profileImage
    const name = author.displayName
    if(url.match(/\.(jpeg|jpg|gif|png)$/) != null) {
      return (
        <Avatar alt={name} src={url} />
      );      
    }

    else {
      return (
        <Avatar sx={{ bgcolor: red[500] }}>
          {name[0]}
        </Avatar>
      );
    }
  }

  const checkContent = () => {
    if (contentType === "text/markdown") {
      return (<ReactCommonmark source={content}/>);
    }
    else if (contentType === "text/plain") {
      return (content);
    }
  }


  return (
    <div className="Post">
      <Card className="Card" variant="outlined">
        <CardHeader
          avatar={
            checkProfileImage()
          }
          title={title}
          subheader={name}
        />
        <CardMedia
          component="img"
          width="5rem"
          image={img}
          style={{ display: checkImageExists(img) }}
        />
        { }

        <CardContent>
          <Typography variant="body2" color="text.primary">
            {checkContent()}
          </Typography>
        </CardContent>

        <CardActions className="CardActions">
          {/* <IconButton aria-label="like" onClick={handleLike}> */}
          {displayLike(id, "post.")}
          {/* </IconButton> */}
          <IconButton aria-label="comment" onClick={handleClickOpenCommentDialog}>
            <ChatBubbleOutlineIcon />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
          {checkFromProfile()}
        </CardActions>
      </Card>

      {/* Dialog for comments */}
      <Dialog
        open={openCommentDialog}
        onClose={handleCloseCommentDialog}
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Comments on {name}'s post</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {commentsForPost && commentsForPost.length > 0 && commentsForPost.map((val) => (
              <div key={val.id}>
                <ListItem
                  key={val.id}
                  disableGutters
                >
                  <ListItemText primary={val.comment} secondary={val.author.displayName} />
                  {/* <IconButton aria-label="like" onClick={handleLike}>
                    {displayLike(val.id)}
                  </IconButton> */}
                  {displayLike(val.id, "comment.")}
                </ListItem>
                <Divider />
              </div>
            ))}
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Add Comment"
            type="comment"
            fullWidth
            variant="standard"
            onChange={handleChangeComment}
            style={{ display: checkIfLoggedIn() }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCommentDialog}>Cancel</Button>
          <Button onClick={handleSubmitComments} style={{ display: checkIfLoggedIn() }}>Comment</Button>
        </DialogActions>
      </Dialog>

      {/* Dialog for editing post */}
      <Dialog
        open={openEditDialog}
        onClose={handleCloseEditDialog}
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Edit Post</DialogTitle>
        <DialogContent>
          <CreateNewPost
            id={id}
            name={name}
            user={user}
            author={author}
            title={title}
            description={description}
            contentType={contentType}
            content={content}
            img={img}
            visibility={visibility}
            newPost={false}
            closeDialog={handleCloseEditDialog}
          />
        </DialogContent>
        <DialogActions>
          {/* <Button onClick={handleCloseEditDialog}>Cancel</Button>
          <Button onClick={handleSubmitEdit}>Save</Button> */}
        </DialogActions>
      </Dialog>

      <Snackbar
        anchorOrigin={{ vertical, horizontal }}
        openCommentDialog={openSnackBar}
        autoHideDuration={6000}
        onClose={handleCloseSnackBar}
        key={vertical + horizontal}
      >
        <Alert severity="success" onClose={handleCloseSnackBar}>Comment Posted</Alert>
      </Snackbar>

    </div>
  );
}

export default Post;

Post.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  author: PropTypes.object.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  contentType: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
  img: PropTypes.string,
  fromProfile: PropTypes.bool.isRequired,
  commentsURL: PropTypes.string.isRequired,
  visibility: PropTypes.string.isRequired,
}