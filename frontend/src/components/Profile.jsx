import { Avatar, Button, Dialog, DialogActions, DialogContent, DialogTitle, Divider, IconButton, List, ListItem, ListItemText, Tab, Tabs } from "@mui/material";
import React, { useState, useEffect } from "react";
import Post from "./Post";
import "./Profile.css"
import axiosInstance from "../axiosInstance";
import axios from "axios";
import { red } from "@mui/material/colors";
import AddIcon from '@mui/icons-material/Add';
import CreateNewPost from "./CreateNewPost";
import FriendItem from "./FriendItem";

function Profile() {
  const [openCreateDialog, setOpenCreateDialog] = useState(false);
  const [allPosts, setAllPosts] = useState([]);
  const [allFollowers, setAllFollowers] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);
  const [allFriends, setAllFriends] = useState([]);
  const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const getFollowers = () => {
    const url = "authors/" + authorId + "/followers/"
    // axios.get(baseURL).then((response) => {
    //   setAllFollowers(response.data.items);
    //   getFriends();
    // });
    axiosInstance.get(url)
      .then((response) => {
        setAllFollowers(response.data.items);
        console.log("AllFollowers:", allFollowers);
        getFriends(response.data.items);
      });
  }

  const getFriends = (followers) => {
    console.log("GetFriends");
    console.log("All followers length,", followers)
    const friends = [];
    const promises = [];

    for (let i = 0; i < followers.length; i++) {
      const followerID = followers[i].id.split("/").pop();
      const url = "authors/" + followerID + "/followers/" + authorId;
      console.log("in loop")

      promises.push(new Promise((resolve, reject) => {
        axiosInstance.get(url)
          .then((response) => {
            if (!response.data.detail) {
              friends.push(followers[i]);
            }
            console.log(allFriends);
            resolve();
          })

      }));
    }

    Promise.all(promises).then((resolve) => {
      setAllFriends(friends);
      console.log("All Friends:", allFriends)
    })

  }

  const getPosts = () => {
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
    // getFriends();
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
    if (allFollowers.length === 0) {
      return true
    }
    return false;
  }

  function checkNoFriends() {
    if (allFriends.length === 0) {
      return true
    }
    return false
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
          {name[0]}
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

  // HANDLE CREATE POST DIALOG
  const handleOpenCreateDialog = () => {
    setOpenCreateDialog(true);
  };

  const handleCloseCreateDialog = () => {
    setOpenCreateDialog(false);
    getPosts();
  };

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
      <div className="NewPost">
        <Button variant="contained" onClick={handleOpenCreateDialog}>CREATE NEW POST</Button>
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
              reloadPosts={getPosts}
              post={val}
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
              <div>
                {checkNoFollowers() ?
                  <List>
                    <ListItem key={"none"} disableGutters >
                      <ListItemText primary={"No followers."} />
                    </ListItem>
                  </List>
                  : <List>
                    {allFollowers.map((value) => (
                      <div key={value.id}>
                        <ListItem key={value.id} disableGutters >
                          <ListItemText primary={value.displayName} />
                        </ListItem>
                        <Divider />
                      </div>
                    ))}
                  </List>
                }
              </div>
            )}
            {tabIndex === 1 && (
              <div>
                {checkNoFriends() ?
                  <List>
                    <ListItem key={"none"} disableGutters >
                      <ListItemText primary={"No friends."} />
                    </ListItem>
                  </List>
                  :
                  <List>
                    {allFriends.map((value) => (
                      // <div key={value.id}>
                      //   <ListItem key={value.id} disableGutters >
                      //     <ListItemText primary={value.displayName} />
                      //   </ListItem>
                      //   <Divider />
                      // </div>
                      <FriendItem 
                      id={value.id}
                      displayName={value.displayName}
                      reloadFriends={getFollowers}
                      />

                    ))}
                  </List>
                }
              </div>
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

      {/* Dialog for creating new post */}
      <Dialog
        open={openCreateDialog}
        onClose={handleCloseCreateDialog}
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Create New Post</DialogTitle>
        <DialogContent>
          <CreateNewPost
            id=""
            name=""
            user=""
            author={{}}
            title=""
            description=""
            contentType=""
            content=""
            img=""
            visibility=""
            newPost={true}
            closeDialog={handleCloseCreateDialog}
          />
        </DialogContent>
        <DialogActions>
          {/* <Button onClick={handleCloseCreateDialog}>Cancel</Button>
              <Button onClick={handleCloseCreateDialog}>Save</Button> */}
        </DialogActions>
      </Dialog>

    </div>
  );
}

export default Profile;
