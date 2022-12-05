import { Card, CardContent, CardHeader, Typography, List, ListItem, ListItemText, Button, CardActions } from "@mui/material";
import axios from "axios";
import React, { useState } from "react";
import { useEffect } from "react";
import axiosInstance from "../axiosInstance";
import FriendRequest from "./FriendRequest";
import Post from "./Post";
import './PublicStream.css';
var isGithubUrl = require('is-github-url');

function Inbox() {
  const [allGithubItems, setAllGithubItems] = useState([]);
  const [allInboxItems, setAllInboxItems] = useState([]);
  const authorId = localStorage.getItem("authorId");
  const authorObject = JSON.parse(localStorage.getItem("author"));

  function checkGithub(url) {

    if (isGithubUrl(url)) {

      if (isGithubUrl(url, { repository: true })) {

        return false
      }

      if (isGithubUrl(url, { strict: true })) {

        return false
      }

      return true
    }
    else {

      return false
    }
  }

  function getGithubActivity() {
    const gitflag = checkGithub(authorObject.github)

    if (gitflag === true) {
      const gitURL = new URL(authorObject.github)
      const username = gitURL.pathname.slice(1)
      const apiURL = "https://api.github.com/users/" + username + "/events/public?per_page=3"
      axios.get(apiURL).then((response) => {
        console.log("Response Github Data");
        console.log(response.data)
        const json = response.data;
        const data = []
        for (let i = 0; i < response.data.length; i++) {
          let obj = json[i];
          data.push({ "user": obj.actor.display_login, "type": obj.type, "repo": obj.repo.name, "created_at": obj.created_at })
        }
        setAllGithubItems(data);
      });
      console.log(allGithubItems)
    }
  }

  const getInboxItems = () => {
    const url = "authors/" + authorId + "/inbox/"

    // axios.get(baseURL).then((response) => {
    //   console.log("REsponse Data");
    //   console.log(response.data);
    //   setAllInboxItems(response.data.items);
    // });
    // console.log(allInboxItems);
    axiosInstance.get(url).then((response) => {
      console.log("Response Data");
      console.log(response.data);
      setAllInboxItems(response.data.items);
    });
    console.log(allInboxItems);
  }

  useEffect(() => {
    getInboxItems();
    getGithubActivity();
    console.log(allInboxItems)
    console.log(allGithubItems)
  }, []);

  function checkImageExists(val) {
    console.log(allInboxItems)
    if (val.contentType === "image/png;base64" || val.contentType === "image/jpeg;base64") {
      return val.content
    }
    else {
      return null;
    }
  }

  const inboxItemType = (val) => {
    if (val.type === 'post') {
      return (
        <Post
          id={val.id}
          name={val.author.displayName}
          user={val.author.id}
          author={val.author}
          title={val.title}
          description={val.description}
          contentType={val.contentType}
          content={val.content}
          img={checkImageExists(val)}
          from={"inbox"}
          commentsURL={val.comments}
          visibility={val.visibility}
          reloadPosts={getInboxItems}
        />
      );
    } else if (val.type === "Follow") {
      return (
        <FriendRequest
          followerURL={val.actor.id}
          summary={val.summary}
          reloadPosts={getInboxItems}
        />
      );
    } else {
      return (
        <Card className="Card" variant="outlined">
          <CardContent>
            <Typography variant="body2" color="text.primary">
              {val.summary}
            </Typography>
          </CardContent>
        </Card>
      );
    };
  };


  const githubItemType = (val) => {
    return (
      <Card className="Card" variant="outlined">
        <CardContent>
          <List>
            <ListItem disablePadding>
              <ListItemText primary="Username" secondary={val.user} />
            </ListItem>
            <ListItem disablePadding>
              <ListItemText primary="Repository" secondary={val.repo} />
            </ListItem>
            <ListItem disablePadding>
              <ListItemText primary="Action" secondary={val.type} />
            </ListItem>
            <ListItem disablePadding>
              <ListItemText primary="Created At" secondary={val.created_at} />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    );
  }


  return (
    <div className="StreamOfPosts">
      <h1>Inbox</h1>
      {allGithubItems.map((val) => (
        githubItemType(val)
      ))}
      {allInboxItems.map((val) => (
        inboxItemType(val)
      ))}
    </div>
  );
}

export default Inbox;