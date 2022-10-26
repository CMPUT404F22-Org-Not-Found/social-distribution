import { Button, TextField } from "@mui/material";
import React from "react";
import "./CreateNewPost.css"

function CreateNewPost() {

  return (
    <div className="CreateNewPost">
      <h1>Create a New Post</h1>
      <div className="PostsContent">
        <TextField className="TextInput" id="outline-multiline-flexible" label="Post Text" multiline rows={10} />
        <div className="UploadImage">
          <Button variant="contained" component="label">
            Upload Image
            <input type="file" hidden />
          </Button>
        </div>
        <div className="ActionButtons">
          <Button variant="outlined">Cancel</Button>
          <Button variant="contained">Post</Button>
        </div>
      </div>
    </div>
  );
}

export default CreateNewPost;