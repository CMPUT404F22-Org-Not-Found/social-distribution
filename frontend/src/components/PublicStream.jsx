import React, { useState, useEffect } from "react";
import './PublicStream.css';
import Post from "./Post";
// import Topbar from "./Topbar";
// import FriendRequests from "./FriendRequests";
import axiosInstance from "../axiosInstance";
import axios from "axios";

function PublicStream() {
  // const [counter, setCounter] = useState(0);
  const [allPosts, setAllPosts] = useState([]);
  const [commentsForPost, setCommentsForPost] = useState([]);

  const samplePosts = [
    {
      name: 'Urvi Patel',
      user: 'urvipatel12',
      content: 'This is my first post on this app. So cool!',
      img: 'null',
      alt: 'null',
      date: 'September 10, 2022',
    },
    {
      name: 'Adit Rada',
      user: 'aditr',
      content: 'This app is just like twitter.',
      img: 'null',
      alt: 'null',
      date: 'Oct 22, 2022',
    },
    {
      name: 'Sanjeev Kotha',
      user: 'skotha',
      content: 'Look at this new recipe I made!',
      img: 'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f',
      alt: 'Snacks',
      date: 'Oct 10, 2022',
    },
  ]

  function getPosts() { 
    // axiosInstance.get(`/authors/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/posts/`)
    // .then((response) => {
    //   setAllPosts(response.data.data);
    //   console.log(allPosts);
    // });
    
    const baseURL = "http://localhost:8000/public/"
    axios.get(baseURL).then((response) => {
      // console.log(response.data.items)
      setAllPosts(response.data.items);
    });
    console.log(allPosts); 
  }

  useEffect(() => {
    getPosts();
    console.log(allPosts);
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
      <h1>Public Posts</h1>
      {allPosts.map((val) => (
        <Post
          key={val.id}
          id={val.id}
          name={val.author.displayName}
          user={val.author.id}
          author={val.author}
          title={val.title}
          description={val.description}
          contentType={val.contentType}
          content={val.content}
          img={checkImageExists(val)}
          from={"public"}
          commentsURL={val.comments}
          visibility={val.visibility}
        />
      ))}
    </div >
  );
}

export default PublicStream;