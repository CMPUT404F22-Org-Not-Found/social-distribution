import { Button, Card, CardActions, CardContent, Divider, List, ListItem, ListItemText, StyledEngineProvider, Typography } from "@mui/material";
import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import axiosInstance from "../axiosInstance";
import PropTypes from 'prop-types';
import './AuthorList';

function FriendRequest(props) {
  const {
    followerURL, summary, reloadPosts,
  } = props

  const [displayAccept, setDisplayAccept] = useState(true);
  const authorId = localStorage.getItem("authorId");

  useEffect(() => {
    checkIfRequestAccepted();
  }, []);

  const acceptFollowRequest = () => {
    const followerID = followerURL.split("/").pop();
    const url = "authors/" + authorId + "/followers/" + followerID;
    const data = {
      author_id: authorId,
      foreign_id: followerID,
    }

    console.log("accepting request")
    axiosInstance.put(url, data)
      .then((response) => {
        console.log("Accept:", response)
        setDisplayAccept(false);
        reloadPosts();
      });
  }

  const checkIfRequestAccepted = () => {
    // make axios call to check if friend request had already been accepted.
    const followerID = followerURL.split("/").pop();
    const url = "authors/" + authorId + "/followers/" + followerID;
    let accepted = false;

    axiosInstance.get(url)
      .then((response) => {
        console.log("Request Check:", response)

        console.log("ResponseDetail:", response.data.detail === undefined)
        if (response.data.detail === undefined) {
          // if detail field is undefined, then friend request had been accepted
          accepted = true;
          setDisplayAccept(false);
        }
      });
  } 

  const checkDisplayAccept = () => {
    // check if image needs to be displayed
    let style = '';
    if (!displayAccept) {
      style = 'none'
    }
    return style;
  }
  const checkDisplay = () => {
    // check if image needs to be displayed
    let style = '';
    if (displayAccept) {
      style = 'none'
    }
    return style;
  }

  return (
    <Card className="FollowCard" variant="outlined">
      <CardContent>
        <Typography variant="body2" color="text.primary">
          {summary}
        </Typography>
      </CardContent>
      <CardActions>
        <Button  style={{ display: checkDisplay() }} disabled>Request Accepted</Button>
        <Button  style={{ display: checkDisplayAccept() }} onClick={acceptFollowRequest}>Accept</Button>
      </CardActions>
    </Card>

  );
}

export default FriendRequest;

FriendRequest.propType = {
  followerURL: PropTypes.string.isRequired,
  summary: PropTypes.string.isRequired,
  reloadPosts: PropTypes.func.isRequired,
}
