import { Button, Divider, List, ListItem, ListItemText, StyledEngineProvider } from "@mui/material";
import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import './AuthorList.css';

function AuthorList() {
  const [allAuthorList, setAllAuthorList] = useState([]);

  function getAuthorList() {
    const baseURL = "http://localhost:8000/authors/"
    axios.get(baseURL).then((response) => {
      setAllAuthorList(response.data.items);
    });
  }

  function onClickSendRequest() {
    
  }

  useEffect(() => {
    getAuthorList();
    console.log(allAuthorList);
  }, []);

  return (
    <StyledEngineProvider injectFirst>
      <div className="AuthorList">
        <h1>Phone Book</h1>
        <div className="AuthorList">
          <List>
            {allAuthorList.map((value) => (
              <div>
                <ListItem
                  key={value.displayName}
                  disableGutters
                  secondaryAction={
                    <div className="RequestButtons">
                      <div>
                        <Button 
                        variant="contained" 
                        onClick={onClickSendRequest}>Send Request</Button>
                      </div>
                    </div>
                  }
                >
                  <ListItemText primary={value.displayName} />
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

export default AuthorList;