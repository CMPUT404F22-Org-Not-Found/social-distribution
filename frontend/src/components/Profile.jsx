import { Divider, List, ListItem, ListItemText } from "@mui/material";
import React from "react";
import Post from "./Post";
import "./Profile.css"

function Profile() {

  const sampleFriendList = [
    {
      name: 'Marzookh',
    },
    {
      name: 'Adit',
    }
  ]

  return (
    <div className="Profile">
      <h1>My Profile</h1>
      <div className="Content">
        <div className="MyPosts">
          <Post />
        </div>
        <div className="MyFriends">
          <h3>My Friends</h3>
          <List className="List">
            {sampleFriendList.map((value) => (
              <div>
                <ListItem key={value.name} disableGutters >
                  <ListItemText primary={value.name} />
                </ListItem>
                <Divider />
              </div>
            ))}
          </List>
        </div>
      </div>

    </div>
  );
}

export default Profile;