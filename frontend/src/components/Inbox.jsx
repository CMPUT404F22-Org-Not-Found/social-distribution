import axios from "axios";
import React, { useState } from "react";
import { useEffect } from "react";
import Post from "./Post";
import './PublicStream.css';



function Inbox() {
  const [allInboxPosts, setAllInboxPosts] = useState([]);

  function getInboxPosts() {
    const baseURL = "http://localhost:8000/author/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/inbox/"

    axios.get(baseURL).then((response) => {
      setAllInboxPosts(response.data.items);
    });
  }

  useEffect(() => {
    getInboxPosts();
    console.log(allInboxPosts)
  }, []);

  function checkImageExists(val) {
    if (val.contentType === "image/png;base64" || val.contentType === "image/jpeg;base64") {
      return val.content
    }
    else {
      return null;
    }
  }


  return (
    <div className="StreamOfPosts">
      <h1>Inbox</h1>
      {allInboxPosts.map((val) => (
        <Post
          name={val.author.displayName}
          user={val.author.id}
          content={val.description}
          img={checkImageExists(val)}
          alt={null}
          date={'Oct 26, 2022'}
          fromProfile={true}
          comments={val.comments}
        />
      ))}
    </div>
  );
}

export default Inbox;