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

function Post(props) {
  const [open, setOpen] = useState(false);
  const [commentsForPost, setCommentsForPost] = useState([]);
  const [newComment, setNewComment] = useState("");

  const {
    name, user, author, content, img, alt, date, fromProfile, comments
  } = props

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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (event) => {
    setNewComment(event.target.value);
  }

  const handleSubmit = () => {
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
        handleClose();
        handleOpenSnackBar({
          vertical: 'top',
          horizontal: 'center',
        });
      });
    console.log(postData);
    console.log(comments);
    handleClose();
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
        <IconButton aria-label="edit">
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
          title={user}
          subheader={date}
        />
        <CardMedia
          component="img"
          width="5rem"
          image={img}
          alt={alt}
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
          <IconButton aria-label="comment" onClick={handleClickOpen}>
            <ChatBubbleOutlineIcon />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
          {checkFromProfile()}
        </CardActions>
      </Card>
      <Dialog
        open={open}
        onClose={handleClose}
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
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit}>Comment</Button>
        </DialogActions>
      </Dialog>
      <Snackbar
        anchorOrigin={{ vertical, horizontal }}
        open={openSnackBar}
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
  name: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  author: PropTypes.object.isRequired,
  content: PropTypes.string.isRequired,
  img: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  fromProfile: PropTypes.bool.isRequired,
  comments: PropTypes.string.isRequired,
}