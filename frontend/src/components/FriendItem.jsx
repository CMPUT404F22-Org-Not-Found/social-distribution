import React from "react";
import PropTypes from 'prop-types';
import { Button, Divider, ListItem, ListItemButton, ListItemText } from "@mui/material";
import axiosInstance from "../axiosInstance";


function FriendItem(props) {
  const {
    id, displayName, reloadFriends,
  } = props

  const foreignId = localStorage.getItem("authorId");

  const removeFriend = () => {
    const authorId = id.split("/").pop();
    const url = "authors/" + authorId + "/followers/" + foreignId;
    const data = {
      author_id: authorId,
      foreign_id: foreignId,
    }

    console.log("deleting request at:", url)
    axiosInstance.delete(url, data)
      .then((response) => {
        console.log("Deleted:", response)
        reloadFriends();
      });
  }

  return (
    <div key={foreignId}>
      <ListItem key={foreignId} disableGutters >
        <ListItemText primary={displayName} />
        <Button onClick={removeFriend}>Remove Friend</Button>
      </ListItem>
      <Divider />
    </div>
  )
}

export default FriendItem;

FriendItem.propType = {
  id: PropTypes.string.isRequired,
  displayName: PropTypes.string.isRequired,
  reloadFriends: PropTypes.func.isRequired,
}