import { Avatar, Divider, List, ListItem, ListItemText, Tab, Tabs } from "@mui/material";
import React, { useState, useEffect } from "react";
import Post from "./Post";
import "./Profile.css"
import axiosInstance from "../axiosInstance";
import axios from "axios";
import { red } from "@mui/material/colors";

function Profile() {
  const [allPosts, setAllPosts] = useState([]);
  const [allFollowers, setAllFollowers] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);
  const [allFriends, setAllFriends] = useState([]);
  const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const sampleFriendList = [
    {
      id: '1',
      displayName: 'Marzookh',
    },
    {
      id: '2',
      displayName: 'Adit',
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

  function getFollowers() {
    const url = "authors/" + authorId + "/followers/"
    // axios.get(baseURL).then((response) => {
    //   setAllFollowers(response.data.items);
    //   getFriends();
    // });
    axiosInstance.get(url).then((response) => {
      setAllFollowers(response.data.items);
      getFriends();
    });
  }

  const getFriends = () => {
    console.log("GetFriends");
    const friends = [];
    const promises = [];

    for (let i = 0; i < allFollowers.length; i++) {
      const url = "authors/" + allFollowers[i].id + "/followers/c01ade2f-49ec-4889-8ecf-a461cd8d5e31";

      promises.push(new Promise((resolve) => {
        axiosInstance.get(url)
          .then((response) => {
            if (!response.data.detail) {
              friends.push(allFollowers[i]);
            }
            console.log(friends);
            resolve();
          })
      }));
    }

    Promise.all(promises).then((response) => {
      setAllFriends(friends);
      console.log(allFriends)
    })

  }

  function getPosts() {
    const params = {
      id: '...',
    };

    // axiosInstance.get(`/authors/c01ade2f-49ec-4889-8ecf-a461cd8d5e31/posts/`)
    // .then((response) => {
    //   setAllPosts(response.data.data);
    //   console.log(allPosts);
    // });
    const url = "authors/" + authorId + "/posts/"
    // axios.get(baseURL).then((response) => {
    //   setAllPosts(response.data.items);
    // });
    // console.log(allPosts);
    axiosInstance.get(url).then((response) => {
      setAllPosts(response.data.items);
    });
    console.log(allPosts);
  }

  useEffect(() => {
    getPosts();
    console.log(allPosts);
    getFollowers();
    console.log(allFollowers);
  }, []);


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

  function checkImageExists(val) {
    if (val.contentType === "image/png;base64" || val.contentType === "image/jpeg;base64") {
      return val.content
    }
    else {
      return null;
    }
  }

  function checkNoFollowers() {
    let style = 'none';
    if (allFollowers.length === 0) {
      style = ' ';
    }
    return style;
  }

  // https://codingbeautydev.com/blog/material-ui-tabs/
  const handleTabChange = (event, newTabIndex) => {
    setTabIndex(newTabIndex);
  }

  const checkProfileImage = () => {
     const url = authorObject.profileImage
     const name = authorObject.displayName
      if (url !== null && (url.match(/\.(jpeg|jpg|gif|png)$/) !== null)) {
       return (
         <Avatar alt={name} src={url} />
       );      
     }

    else {
      return (
        <Avatar sx={{ bgcolor: red[500] }}>
          {authorObject.displayName[0]}
        </Avatar>
      );
     }
  }

  const checkGithubExists = () => {
    const github = authorObject.github;
    if (github !== null) {
      return (
        <div className="ProfileData">
          <h4>Github: </h4>
          <p className="data">{github}</p>
        </div>
      )
    } else {
        return (
          <div className="ProfileData">
            <h4>Github: </h4>
            <p className="data">NO GITHUB SPECIFIED</p>
          </div>
        )
    }
  }

  return (
    <div className="Profile">
      <h1>My Profile</h1>
      <div className="PersonalInfo">
        {checkProfileImage()}
        <div>
          <div className="ProfileData">
            <h4>Display Name: </h4>
            <p className="data">{authorObject.displayName}</p>
          </div>
          {checkGithubExists()}
        </div>
      </div>
      <div className="Content">
        <div className="MyPosts">
          <h3>My Posts</h3>
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
              from={"profile"}
              commentsURL={val.comments}
              visibility={val.visibility}
            />
          ))}
        </div>
        <div>
          <div>
            <Tabs value={tabIndex} onChange={handleTabChange}>
              <Tab label="Followers" />
              <Tab label="Friends" />
            </Tabs>
          </div>
          <div>
            {tabIndex === 0 && (
              <List>
                <ListItem style={{ display: checkNoFollowers() }} key={"none"} disableGutters >
                  <ListItemText primary={"No followers."} />
                </ListItem>
                {allFollowers.map((value) => (
                  <div key={value.id}>
                    <ListItem key={value.id} disableGutters >
                      <ListItemText primary={value.displayName} />
                    </ListItem>
                    <Divider />
                  </div>
                ))}
              </List>
            )}
            {tabIndex === 1 && (
              <List>
                <ListItem style={{ display: checkNoFollowers() }} key={"none"} disableGutters >
                  <ListItemText primary={"No friends."} />
                </ListItem>
                {allFriends.map((value) => (
                  <div key={value.id}>
                    <ListItem key={value.id} disableGutters >
                      <ListItemText primary={value.displayName} />
                    </ListItem>
                    <Divider />
                  </div>
                ))}
              </List>
            )}
          </div>
        </div>
        <div className="MyFriends">
          {/* <h3>Followers</h3>
          <div className="List">
            <List>
              <ListItem style={{ display: checkNoFollowers() }} key={"none"} disableGutters >
                <ListItemText primary={"No followers."} />
              </ListItem>
              {allFollowers.map((value) => (
                <div>
                  <ListItem key={value.id} disableGutters >
                    <ListItemText primary={value.displayName} />
                  </ListItem>
                  <Divider />
                </div>
              ))}
            </List>
          </div> */}
        </div>
      </div>

    </div >
  );
}

export default Profile;
