import { Avatar, Card, CardActions, CardContent, CardHeader, CardMedia, IconButton, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';

import React from "react";
import './Post.css';

function Post() {
  const samplePosts = [
    {
      name: 'Urvi Patel',
      user: 'urvipatel12',
      content: 'This is my first post on this app. So cool!',
      img: null,
      alt: null,
      date: 'September 10, 2022',
    },
    {
      name: 'Adit Rada',
      user: 'aditr',
      content: 'This app is just like twitter.',
      img: null,
      alt: null,
      date: 'Oct 22, 2022',
    },
    {
      name: 'Sanjeev Kotha',
      user: 'skotha',
      content: 'Look at this new recipe I made!',
      img: 'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f',
      alt: 'Snacks',
      date: 'Oct 10, 2022',
    },
  ]

  function checkImageExists(image) {
    let style = '';
    if (image === null) {
      style = 'none'
    }
    return style
  }

  return (
    <div className="Post">
      {samplePosts.map((val) => (
        <Card className="Card" variant="outlined">
          <CardHeader
            avatar={
              <Avatar sx={{ bgcolor: red[500] }}>
                {val.name[0]}
              </Avatar>
            }
            title={val.user}
            subheader={val.date}
          />
          <CardMedia
            component="img"
            width="5rem"
            image={val.img}
            alt={val.alt}
            style={{ display: checkImageExists(val.img) }}
          />
          {}

          <CardContent>
            <Typography variant="body2" color="text.primary">
              {val.content}
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
      ))}
    </div>
  );
}

export default Post;