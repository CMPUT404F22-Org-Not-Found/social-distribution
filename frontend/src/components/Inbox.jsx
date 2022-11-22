import { Card, CardContent, CardHeader, Typography } from "@mui/material";
import axios from "axios";
import React, { useState } from "react";
import { useEffect } from "react";
import Post from "./Post";
import './PublicStream.css';

function Inbox() {
  const [allInboxItems, setAllInboxItems] = useState([]);

  function getInboxItems() {
    const baseURL = "http://localhost:8000/authors/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/inbox/"

    axios.get(baseURL).then((response) => {
      console.log("REsponse Data");
      console.log(response.data);
      setAllInboxItems(response.data.items);
    });
    console.log(allInboxItems);
  }

  useEffect(() => {
    getInboxItems();
    console.log(allInboxItems)
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
      if (val.type == 'post') {
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
          fromProfile={false}
          comments={val.comments}
          visibility={val.visibility}
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


  return (
    <div className="StreamOfPosts">
      <h1>Inbox</h1>
      {allInboxItems.map((val) => (
        inboxItemType(val)
      ))}
    </div>
  );
}

export default Inbox;