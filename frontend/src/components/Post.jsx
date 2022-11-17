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

function Post(props) {
  const {
    id, name, user, author, title, description, contentType, content, img, fromProfile, comments, visibility,
  } = props

  const [openCommentDialog, setOpenCommentDialog] = useState(false);
  const [commentsForPost, setCommentsForPost] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [openEditDialog, setOpenEditDialog] = useState(false);

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

  const handleSubmitComments = () => {
    const commentDate = new Date();
    const postData = {
      type: "comment",
      author: author,
      comment: newComment,
      contentType: "text/plain",
      published: commentDate.toISOString(),
    };

    axios.post(comments + "/", postData)
      .then((response) => {
        handleCloseCommentDialog();
        handleOpenSnackBar({
          vertical: 'top',
          horizontal: 'center',
        });
      });
    console.log(postData);
    console.log(comments);
    handleCloseCommentDialog();
    handleOpenSnackBar();

    console.log(newComment);
    window.location.reload();
  };

  function checkImageExists(image) {
    let style = '';
    if (image === 'null') {
      style = 'none'
    }
    return style
  }

  const checkFromProfile = () => {
    if (fromProfile) {
      return (
        <IconButton aria-label="edit" onClick={handleOpenEditDialog}>
          <EditIcon />
        </IconButton>
      )
    };
  };

  useEffect(() => {
    getCommentsForPost(comments);
    console.log(commentsForPost);
  }, []);



  function getCommentsForPost(commentsUrl) {
    console.log(commentsUrl);
    axios.get(commentsUrl + "/").then((response) => {
      console.log(response.data.comments);
      setCommentsForPost(response.data.comments);
    });
    console.log(commentsForPost);
    return commentsForPost;
  }

  const handleLike = () => {
    // check if the post had been liked by the current user
    // if yes, delete like
    // if no, post new like
  };

  const displayLike = () => {
    return (
      <FavoriteIcon />
    );
    // return(
    // <FavoriteBorderIcon />
    // );
  };

  return (
    <div className="Post">
      <Card className="Card" variant="outlined">
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }}>
              {name[0]}
            </Avatar>
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
            {content}
          </Typography>
        </CardContent>

        <CardActions className="CardActions">
          <IconButton aria-label="like" onClick={handleLike}>
            {displayLike()}
          </IconButton>
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
              <div>
                <ListItem
                  key={val.id}
                  disableGutters
                >
                  <ListItemText primary={val.comment} secondary={val.author.displayName} />
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
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCommentDialog}>Cancel</Button>
          <Button onClick={handleSubmitComments}>Comment</Button>
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
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog}>Cancel</Button>
          <Button onClick={handleSubmitEdit}>Save</Button>
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
  img: PropTypes.string.isRequired,
  fromProfile: PropTypes.bool.isRequired,
  comments: PropTypes.string.isRequired,
  visibility: PropTypes.string.isRequired,
}