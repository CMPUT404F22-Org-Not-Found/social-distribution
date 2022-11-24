import { Button, TextField } from "@mui/material";
import React from "react";
import { useState } from "react";
import "./CreateNewPost.css"
import axios from "axios";

function CreateNewPost() {

  const [post, setPosts] = useState([]);
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [content, setContent] = useState('');
  const [ctype, setCtype] = useState('');
  const [categories, setCategories] = useState([]);
  const [visibility, setVisibility] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    addPost(title, desc, content, ctype, categories, visibility);
  }

  const addPost = (title, desc, content, ctype, categories, visibility) => {
    const postData = {
      type: "post",
      title: title,
      description: desc,
      contentType: ctype,
      content: content,
      categories: categories,
      visibility: visibility
    };

    setTitle('');
    setDesc('');
    setCtype('');
    setContent('');
    setCategories([]);
    setVisibility('');

    axios.post(post + "/", postData)
    console.log(postData);
    console.log(content)
  };

  return (
    <div className="CreateNewPost">
      <h1>Create a New Post</h1>
      <div className="PostsContent">
        <TextField className="TextInput" id="outlined-basic" label="Title"/>
        <TextField className="TextInput" id="outlined-basic" label="Description"/>
        <TextField className="TextInput" id="outline-multiline-flexible" label="Post Text" multiline rows={10} />
        <TextField className="TextInput" id="outlined-basic" label="Categories"/>
        <FormControl fullWidth>
        <InputLabel id="visibility-select">Visibility</InputLabel>
          <Select
            labelId="visibility-select"
            id="visibility-select"
            value={visibility}
            label="Visibility"
            onChange={handleChange}
          >
            <MenuItem value={"Public"}>Public</MenuItem>
            <MenuItem value={"Friends"}>Friends</MenuItem>
          </Select>
        </FormControl>
        <div className="UploadImage">
          <Button variant="contained" component="label">
            Upload Image
            <input type="file" hidden />
          </Button>
        </div>
        <div className="ActionButtons">
          <Button variant="outlined">Cancel</Button>
          <Button variant="contained" onClick={handleSubmit}>Post</Button>
        </div>
      </div>
    </div>
  );
}

export default CreateNewPost;