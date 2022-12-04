import { Button, FormControl, FormControlLabel, FormLabel, InputLabel, MenuItem, Radio, RadioGroup, Select, TextField } from "@mui/material";
import React from "react";
import { useState } from "react";
import "./CreateNewPost.css"
import PropTypes from 'prop-types';
import axios from "axios";
import axiosInstance from "../axiosInstance";

function CreateNewPost(props) {

  const {
    id, name, user, author, title, description, contentType, content, img, visibility, newPost, closeDialog
  } = props

  // const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const [titleText, setTitle] = useState(title);
  const [descriptionText, setDescription] = useState(description);
  const [inputType, setInputType] = useState(contentType);
  const [contentText, setContent] = useState(content);
  const [visibilityType, setVisibility] = useState(visibility);

  const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

  const handleTitleChange = (event) => {
    setTitle(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
  };

  const handleInputTypeChange = (event) => {
    setInputType(event.target.value);
    // if (event.target.value === "image/png;base64" || event.target.value === "image/jpeg;base64") {
    //   setContent("");
    // }
  };

  const handleContentChange = (event) => {
    setContent(event.target.value);
  };

  const handleVisibilityChange = (event) => {
    setVisibility(event.target.value);
  };

  const allFilled = () => {
    // check if all the fields are filled in
    if (titleText != "" && descriptionText != "" && inputType != "" && contentText != "" && visibilityType != "") {
      return true;
    }
    return false;
  };

  const ifEditPost = () => {
    // if not a new post, show delete button
    if (!newPost) {
      return (
        <Button className="DeleteButton" variant="contained" onClick={confirmDelete}>DELETE</Button>
      );
    }
  }

  const typeOfPost = () => {
    // check if new post or post already exists
    if (newPost) {
      return (
        <Button variant="contained" onClick={handleNewPost}>Create Post</Button>
      )
    } else {
      return (
        <Button variant="contained" onClick={handleUpdatePost}>Update Post</Button>
      )
    }
  }

  const handleNewPost = () => {
    //create a new post
    if (allFilled()) {
      console.log("All fields have been filled, make new post")
      const postData = {
        type: "post",
        title: titleText,
        description: descriptionText,
        contentType: inputType,
        content: contentText,
        categories: [],
        visibility: visibilityType,
        unlisted: false,
      };

      console.log("Make axios call for creating a new post.");
      const url = "authors/" + authorId + "/posts/"
      console.log(postData)
      axiosInstance.post(url, postData)
        .then((response) => {
          console.log("created new post")
          console.log(response);
          closeDialog();
        })

    } else {
      console.log("All fields have not been filled. Cannot make post.")
    }
  }

  const handleUpdatePost = () => {
    // update an existing post
    if (allFilled()) {
      console.log("All fields have been filled, update post")

      const postData = {
        title: titleText,
        description: descriptionText,
        contentType: inputType,
        content: contentText,
        visibility: visibilityType,
      };


      // console.log("id:", id);
      const postID = id.split("/")[6];
      // console.log("postid:", postID);
      const url = "authors/" + authorId + "/posts/" + postID + "/";
      // console.log("edit existing post");
      // console.log("Data to post:", postData);
      // console.log(axiosInstance.baseURL + url)
      // console.log("url:", url);
      axiosInstance.post(url, postData)
        .then((response) => {
          console.log("successfully edited post");
          console.log(response);
          // window.location.reload();
          closeDialog();
        });
    } else {
      console.log("All fields have not been filled. Cannot make post.")
    }
  };

  const toggleButtons = () => {
    // toggle buttons if user clicks on delete
    if (showDeleteConfirmation) {
      return (
        <div>
          <h3>Are you sure you would like to delete this post?</h3>
          <Button variant="contained" color="error" onClick={confirmDelete}>No</Button>
          <Button variant="contained" color="success" onClick={handleDeletePost}>Yes</Button>
        </div>
      )
    } else {
      return (
        <div className="ActionButtons">
          <Button variant="outlined" onClick={closeDialog}>Cancel</Button>
          {ifEditPost()}
          {typeOfPost()}
        </div>
      )
    }
  }

  const confirmDelete = () => {
    // show delete confirmation buttons
    if (showDeleteConfirmation) {
      setShowDeleteConfirmation(false);
    } else {
      setShowDeleteConfirmation(true);
    }
  }

  const handleDeletePost = () => {
    // delete the post
    const postID = id.split("/")[6];
    const url = "authors/"+ authorId + "/posts/" + postID + "/";

    axiosInstance.delete(url)
      .then((response) => {
        console.log(response);
        console.log("Deleted post");
        window.location.reload();
      });
  }

  return (
    <div className="CreateNewPost">
      {/* <h1>Create a New Post</h1> */}
      <div className="PostsContent">
        <div className="formElement">
          <TextField className="TextInput" id="outline-multiline-flixible" label="Title" defaultValue={titleText} onChange={handleTitleChange} />
        </div>
        <div className="formElement">
          <TextField className="TextInput" id="outline-multiline-flexible" label="Description" multiline rows={10} defaultValue={descriptionText} onChange={handleDescriptionChange} />
        </div>
        <div className="formElement">
          <FormControl fullWidth>
            <InputLabel id="demo-simple-select-label">Input Type</InputLabel>
            <Select
              labelId="demo-simple-select-lable"
              value={inputType}
              defaultValue={inputType}
              label="Input Type"
              onChange={handleInputTypeChange}
            >
              <MenuItem value={"text/markdown"}>text/markdown</MenuItem>
              <MenuItem value={"text/plain"}>text/plain</MenuItem>
              <MenuItem value={"application/base64"}>application/base64</MenuItem>
              <MenuItem value={"image/png;base64"}>image/png;base64</MenuItem>
              <MenuItem value={"image/jpeg;base64"}>image/jpeg;base64</MenuItem>
            </Select>
          </FormControl>
        </div>
        <div className="formElement">
          {/* If input type is image, show upload image button*/}
          {inputType === "image/png;base64" || inputType === "image/jpeg;base64" ?
            <div className="UploadImage">
              <Button variant="contained" component="label">
                Upload Image
                <input type="file" hidden />
              </Button>
            </div>
            : ""
          }
        </div>
        <div className="formElement">
          {/* if input type is text or markdown, show inbox button */}
          {inputType === "text/markdown" || inputType === "text/plain" ?
            <TextField className="TextInput" id="outline-multiline-flexible" label="Content" multiline rows={10} defaultValue={contentText} onChange={handleContentChange} />
            : ""
          }
        </div>
        <div className="formElement">
          <FormControl className="VisibilitySelection">
            <FormLabel id="demo-radio-buttons-group-label">Visibility</FormLabel>
            <RadioGroup
              aria-labelledby="demo-radio-buttons-group-label"
              name="radio-buttons-group"
              defaultValue={visibilityType}
              onChange={handleVisibilityChange}
            >
              <FormControlLabel value="PUBLIC" control={<Radio />} label="PUBLIC" />
              <FormControlLabel value="FRIENDS" control={<Radio />} label="FRIENDS" />
            </RadioGroup>
          </FormControl>
        </div>
        <div className="formElement">
          {toggleButtons()}
        </div>
      </div>
    </div>
  );
}

export default CreateNewPost;


CreateNewPost.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  author: PropTypes.object.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  contentType: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
  img: PropTypes.string,
  visibility: PropTypes.string.isRequired,
  newPost: PropTypes.bool.isRequired,
  closeDialog: PropTypes.func.isRequired,
}