import { Button, Divider, List, ListItem, ListItemText, StyledEngineProvider } from "@mui/material";
import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import './FriendRequests.css';
import axiosInstance from "../axiosInstance";

function FriendRequests() {
  const [allFriendRequests, setAllFriendRequests] = useState([]);
  // const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const sampleFriendRequests = [
    {
      name: 'Ervin Joseph',
    },
    {
      name: 'Sanjeev Kotha',
    }
  ]

  function getFriendRequests() {
    const url = "authors/" + authorId + "/followers/friendrequest/"
    // axios.get(url).then((response) => {
    //   setAllFriendRequests(response.data.items);
    // });

    axiosInstance.get(url).then((response) => {
      setAllFriendRequests(response.data.items);
    });
  }

  useEffect(() => {
    getFriendRequests();
    console.log(allFriendRequests);
  }, []);

  return (
    <StyledEngineProvider injectFirst>
      <div className="FriendRequest">
        <h1>Friend Requests</h1>
        <div className="FriendList">
          <List>
            {allFriendRequests.map((value) => (
              <div>
                <ListItem
                  key={value.actor.displayName}
                  disableGutters
                  secondaryAction={
                    <div className="RequestButtons">
                      <div>
                        <Button variant="contained">Accept</Button>
                      </div>
                      <div>
                        <Button variant="contained">Decline</Button>
                      </div>
                    </div>
                  }
                >
                  <ListItemText primary={value.actor.displayName} />
                </ListItem>
                <Divider />
              </div>
            ))}
          </List>
        </div>
      </div >
    </StyledEngineProvider>

  );
}

export default FriendRequests;