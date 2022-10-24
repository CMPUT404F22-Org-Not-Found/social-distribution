import { Button, TextField } from "@mui/material";
import React from "react";
import "./CreateNewPost.css"

function CreateNewPost() {

  return (
    <div className="CreateNewPost">
      <h1>Create a New Post</h1>
      <div className="Content">
        <TextField className="TextInput" id="outline-multiline-flexible" label="Multiline" multiline rows={10} />
        <Button className="UploadImage" variant="contained" component="label">
          Upload Image
          <input type="file" hidden />
        </Button>
        <div className="ActionButtons">
          <Button variant="outlined">Cancel</Button>
          <Button variant="contained">Post</Button>
        </div>
      </div>
    </div>
  );
}

export default CreateNewPost;