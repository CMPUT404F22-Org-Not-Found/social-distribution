import { Avatar, Button, Card, CardActions, CardContent, CardHeader, CardMedia, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, IconButton, ListItem, ListItemText, TextField, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';

import React from "react";
import './Post.css';

function Post(props) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };


  const {
    name, user, content, img, alt, date, fromProfile, comments
  } = props

  function checkImageExists(image) {
    let style = '';
    if (image === 'null') {
      style = 'none'
    }
    return style
  }

  function checkFromProfile() {
    if (fromProfile) {
      return (
        <IconButton aria-label="edit">
          <EditIcon />
        </IconButton>
      )
    }

  }

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
          <IconButton aria-label="like">
            <FavoriteBorderIcon />
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
            {comments.map((val) => (
              <div>
                <ListItem
                  key={val.user}
                  disableGutters
                >
                  <ListItemText primary={val.comment} secondary={val.user} />
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
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleClose}>Comment</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default Post;

Post.propTypes = {
  name: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
  img: PropTypes.string.isRequired,
  alt: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  fromProfile: PropTypes.bool.isRequired,
  comments: PropTypes.array.isRequired,
}