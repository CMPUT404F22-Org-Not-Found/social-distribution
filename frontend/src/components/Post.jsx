import { Avatar, Card, CardActions, CardContent, CardHeader, CardMedia, IconButton, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';

import React from "react";
import './Post.css';

function Post(props) {
  const {
    name, user, content, img, alt, date, fromProfile
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
          <IconButton aria-label="comment">
            <ChatBubbleOutlineIcon />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
          {checkFromProfile()}
        </CardActions>
      </Card>
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
}