import { Avatar, Card, CardActions, CardContent, CardHeader, CardMedia, IconButton, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';

import React from "react";
import './Post.css';

function Post() {
  return (
    <div className="Post">
      <Card className="Card">
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
              Me
            </Avatar>
          }
          title="My User Name"
          subheader="September 14, 2016"
        />
        <CardMedia
          component="img"
          width="5rem"
          image="https://images.unsplash.com/photo-1627308595229-7830a5c91f9f"
          alt="Snacks"
        />

        <CardContent>
          <Typography variant="body2" color="text.secondary">
            These impressive snacks are the perfect fall treat.
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
        </CardActions>
      </Card>
    </div>
  );
}

export default Post;