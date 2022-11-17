import { Button, FormControl, FormControlLabel, FormLabel, InputLabel, MenuItem, Radio, RadioGroup, Select, TextField } from "@mui/material";
import React from "react";
import { useState } from "react";
import "./CreateNewPost.css"
import PropTypes from 'prop-types';
import axios from "axios";

function CreateNewPost(props) {

  const {
    id, name, user, author, title, description, contentType, content, img, visibility, newPost
  } = props


  const [titleText, setTitle] = useState(title);
  const [descriptionText, setDescription] = useState(description);
  const [inputType, setInputType] = useState(contentType);
  const [contentText, setContent] = useState(content);
  const [visibilityType, setVisibility] = useState(visibility);

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
    if (titleText != "" && descriptionText != "" && inputType != "" && contentText != "" && visibilityType != "") {
      return true;
    }
    return false;
  };

  const handlePost = () => {
    if (allFilled()) {
      console.log("All feilds have been filled, make post")
    } else {
      console.log("All fields have not been filled. Cannot make post.")
    }

    const url = author.url + "/posts/" + id + "/";
    const postData = {
      title: titleText,
      description: descriptionText,
      contentType: inputType,
      content: contentText,
      visibility: visibilityType,
    };

    if (newPost) {
      console.log("Make axios call for creating a new post.");

    } else {
      console.log("edit existing post");
      console.log("Data to post:",postData);
      axios.post(url, postData)
      .then((response) => {
        console.log("successfully edited post");
      });

    }


  };

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
              <FormControlLabel value="PUBLIC" control={<Radio />} label="Public" />
              <FormControlLabel value="PRIVATE" control={<Radio />} label="Private" />
            </RadioGroup>
          </FormControl>
        </div>
        <div className="formElement">
          <div className="ActionButtons">
            <Button variant="outlined">Cancel</Button>
            <Button variant="contained" onClick={handlePost}>Post</Button>
          </div>
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
  img: PropTypes.string.isRequired,
  visibility: PropTypes.string.isRequired,
  newPost: PropTypes.bool.isRequired,
}