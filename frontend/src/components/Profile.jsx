import { Divider, List, ListItem, ListItemText } from "@mui/material";
import React, { useState } from "react";
import Post from "./Post";
import "./Profile.css"
import axiosInstance from "../axiosInstance";
import axios from "axios";
import { useEffect } from "react";

function Profile() {
  const [allPosts, setAllPosts] = useState([]);

  const sampleFriendList = [
    {
      name: 'Marzookh',
    },
    {
      name: 'Adit',
    }
  ]

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

  function getPosts(){
    const params = {
      id: '...',
    };

    // axiosInstance.get(`/authors/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/posts/`)
    // .then((response) => {
    //   setAllPosts(response.data.data);
    //   console.log(allPosts);
    // });
    const baseURL = "http://localhost:8000/authors/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/posts/"
    axios.get(baseURL).then((response) => {
      setAllPosts(response.data.items);
    });
    
  }

  useEffect(() => {
    getPosts();
  });


  const sampleComments = [
    {
      user: 'aditr',
      comment: 'Welcome to the app.',
    },
    {
      user: 'skotha',
      comment: 'I love twitter.',
    }
  ]

  return (
    <div className="Profile">
      <h1>My Profile</h1>
      <div className="Content">
        <div className="MyPosts">
          <h3>My Posts</h3>
          {allPosts.map((val) => (
            <Post 
            name={val.author.displayName}
            user={val.author.id}
            content={val.description}
            img={null}
            alt={null}
            date={'Oct 26, 2022'}
            fromProfile={true}
            comments={sampleComments}
            />
          ))}
        </div>
        <div className="MyFriends">
          <h3>My Friends</h3>
          <div className="List">
            <List>
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

    </div >
  );
}

export default Profile;