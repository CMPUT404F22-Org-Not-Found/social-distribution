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
        <div className="FriendList">
          <List>
            {sampleFriendRequests.map((value) => (
              <div>
                <ListItem
                  key={value.name}
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
                  <ListItemText primary={value.name} />
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