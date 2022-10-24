import { Button, Divider, List, ListItem, ListItemText, StyledEngineProvider } from "@mui/material";
import React from "react";
import { useEffect } from "react";
import './FriendRequests.css';

function FriendRequests() {
  const sampleFriendRequests = [
    {
      name: 'Ervin Joseph',
    },
    {
      name: 'Sanjeev Kotha',
    }
  ]

  return (
    <StyledEngineProvider injectFirst>
      <div className="FriendRequest">
        <h1>Friend Requests</h1>
        <List className="List">
          {sampleFriendRequests.map((value) => (
            <div>
              <ListItem
                key={value.name}
                disableGutters
                secondaryAction={
                  <div>
                    <Button variant="contained" className="ActionButton">Accept</Button>
                    <Button variant="contained" className="ActionButton">Decline</Button>
                  </div>
                }
              >
                <ListItemText primary={value.name} />
              </ListItem>
              <Divider />
            </div>
          ))}
        </List>
      </div >
    </StyledEngineProvider>

  );
}

export default FriendRequests;