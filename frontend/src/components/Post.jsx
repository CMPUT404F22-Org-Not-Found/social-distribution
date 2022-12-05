import { Alert, Avatar, Button, Card, CardActions, CardContent, CardHeader, CardMedia, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, FormControl, IconButton, ImageListItem, ImageListItemBar, InputLabel, ListItem, ListItemText, MenuItem, Paper, Select, Snackbar, TextField, Typography } from "@mui/material";
import { red } from "@mui/material/colors";
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline';
import EditIcon from '@mui/icons-material/Edit';
import PropTypes from 'prop-types';
import React, { useState, useEffect, Fragment } from "react"; import './Post.css';
import axios from "axios";
import CreateNewPost from "./CreateNewPost";
import axiosInstance from "../axiosInstance";

var ReactCommonmark = require('react-commonmark');

function Post(props) {
  const {
    id, name, user, author, title, description, contentType, content, img, from, commentsURL, visibility, reloadPosts, post
  } = props

  const [openCommentDialog, setOpenCommentDialog] = useState(false);
  const [commentsForPost, setCommentsForPost] = useState([]);
  const [inputType, setInputType] = useState("");
  const [newComment, setNewComment] = useState("");
  const [openShareDialog, setOpenShareDialog] = useState(false);
  const [allAuthors, setAllAuthors] = useState([]);
  const [authorToSend, setAuthorToSend] = useState("");
  const [openEditDialog, setOpenEditDialog] = useState(false);
  const [allLikedObjects, setAllLikedObjects] = useState([]);
  const authorObject = JSON.parse(localStorage.getItem("author"));
  const authorId = localStorage.getItem("authorId");

  const [stateSnackBar, setStateSnackBar] = useState({
    openSnackBar: false,
    vertical: 'top',
    horizontal: 'center',
  });

  const { vertical, horizontal, openSnackBar } = stateSnackBar;

  const handleOpenSnackBar = () => {
    setStateSnackBar({ openSnackBar: true, ...stateSnackBar });
    console.log("Snackbar opened");
  };

  const handleCloseSnackBar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setStateSnackBar({ ...stateSnackBar, openSnackBar: false });
    console.log("Snackbar closed");
  };

  // HANDLE COMMENT DIALOG
  const handleClickOpenCommentDialog = () => {
    setOpenCommentDialog(true);
  };

  const handleCloseCommentDialog = () => {
    setOpenCommentDialog(false);
  };

  const handleChangeComment = (event) => {
    setNewComment(event.target.value);
  }

  const getCommentsForPost = () => {

    console.log("CommentsURL:", commentsURL);
    axios.get(commentsURL + "/").then((response) => {
      console.log(response.data.comments);
      setCommentsForPost(response.data.comments);
    });
  }

  const handleInputTypeChange = (event) => {
    setInputType(event.target.value);
    // if (event.target.value === "image/png;base64" || event.target.value === "image/jpeg;base64") {
    //   setContent("");
    // }
  };

  const handleSubmitComments = () => {
    // const url = "authors/" + authorId;
    // axiosInstance.get(url).then((response) => {
    //   console.log(response);
    // })
    if (allFilled()) {
      const commentDate = new Date();
      const postData = {
        type: "comment",
        author: authorObject,
        comment: newComment,
        contentType: inputType,
        published: commentDate.toISOString(),
      };

      axiosInstance.post(commentsURL + "/", postData)
        .then((response) => {
          console.log(response);
          document.getElementById("name").value = "";
          getCommentsForPost();

        });

      console.log(postData);
      console.log(commentsURL);

      console.log(newComment);

    } else {
      console.log("All fields have not been filled. Cannot make post.")
    }
  };

  const allFilled = () => {
    // check if all the fields are filled in
    if (inputType != "" && newComment != "") {
      return true;
    }
    return false;
  };

  // HANDLE SHARE DIALOG
  const handleClickOpenShareDialog = () => {
    setOpenShareDialog(true);
  };

  const handleCloseShareDialog = () => {
    setOpenShareDialog(false);
  };

  const getAllAuthors = () => {
    const url = "authors/"

    axiosInstance.get(url)
      .then((response) => {
        console.log(response);
        setAllAuthors(response.data.items)
      })
  };

  const SelectAuthor = (authorID) => {
    if (authorToSend === "") {
      setAuthorToSend(authorID);
    } else {
      setAuthorToSend("");
    }
  };

  const handleSharePost = () => {
    console.log("sharing post to:", authorToSend);
    // add axios call to share post here

    console.log("Sending post:")
    let postID = authorToSend.split("/").pop();

    // const URLtoParse = new URL(authorToSend)
    // if (URLtoParse.hostname === "cmput-404-team-1.herokuapp.com"){
    //   postID = postID.replace(/-/g,"");
    // }

    console.log("Final URL:", postID);

    const postUrl = "authors/" + postID + "/inbox/"
    console.log(post)
    console.log(postUrl)
    console.log("Make axios call to send a share post.");

    axiosInstance.post(postUrl, post)
        .then((response) => {
            console.log("post shared")
            console.log(response);
            setAuthorToSend("");
            handleCloseShareDialog();
        })
  };

  // HANDLE EDIT DIALOG
  const handleOpenEditDialog = () => {
    setOpenEditDialog(true);
  };

  const handleCloseEditDialog = () => {
    setOpenEditDialog(false);
    reloadPosts();
  };

  const handleSubmitEdit = () => {
    const url = author.url + "/posts/" + id + "/";
    const postData = {

    }
  };

  const checkImageExists = (image) => {
    // check if image needs to be displayed
    let style = '';
    if (image === 'null') {
      style = 'none'
    }
    return style;
  }

  const checkFromProfile = () => {
    // check if componenet is being displayed in Profile
    if (from === "profile") {
      return (
        <IconButton aria-label="edit" onClick={handleOpenEditDialog}>
          <EditIcon />
        </IconButton>
      )
    };
  };

  useEffect(() => {
    getCommentsForPost();
    console.log("Comments:", commentsForPost);
    const authToken = window.localStorage.getItem("auth-token");
    if (authToken) {
      getAllLikedObjects();
      console.log()
      console.log("Liked Objects", allLikedObjects);
    }
    getAllAuthors();
    console.log("All Authors", allAuthors);
  }, []);

  // HANDLE LIKING OBJECTS
  const getAllLikedObjects = () => {
    const url = "/authors/" + authorId + "/liked/"
    axiosInstance.get(url)
      .then((response) => {
        const allLikes = response.data.items;

        const objectIds = []
        for (let i = 0; i < allLikes.length; i++) {
          objectIds.push(allLikes[i].object);
        }
        setAllLikedObjects(objectIds);
      });
  }

  const handleLike = (id, type) => {
    // post a new like to the liked object's author's inbox

    const likeData = {
      author: authorObject,
      type: "like",
      summary: authorObject.displayName + " likes your " + type,
      object: id,
    }

    // console.log("ID:", id);
    // // console.log("Like SPLIT ID:", id.split("/"));
    // console.log("Like SPLIT ID -3:", id.split("/").reverse()[2]);
    let objectAuthorID = id.split("/").reverse()[2];

    // const URLtoParse = new URL(id)
    // if (URLtoParse.hostname === "cmput-404-team-1.herokuapp.com"){
    //   objectAuthorID = objectAuthorID.replace(/-/g,"");
    // }

    console.log("Final URL:", objectAuthorID);

    const url = "/authors/" + objectAuthorID + "/inbox/";

    axiosInstance.post(url, likeData)
      .then((response) => {
        console.log(response);
        getAllLikedObjects();
      });
  };

  const displayLike = (id, type) => {
    // check if object has been liked by user, display corresponding icon

    if (allLikedObjects.includes(id)) {
      return (
        <IconButton aria-label="like" style={{ display: checkIfLoggedIn() }}>
          <FavoriteIcon />
        </IconButton>
      );
    } else {
      return (
        <IconButton aria-label="like" onClick={() => handleLike(id, type)} style={{ display: checkIfLoggedIn() }}>
          <FavoriteBorderIcon />
        </IconButton>
      );
    }
  };

  const checkIfLoggedIn = () => {
    // check if token exists, if yes, user is logged in
    const authToken = window.localStorage.getItem("auth-token");
    let style = '';
    if (!authToken) {
      style = 'none'
    }
    return style;
  }

  const checkProfileImage = () => {
    const url = author.profileImage
    const name = author.displayName
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

  const checkContent = () => {
    if (contentType === "text/markdown") {
      return (<ReactCommonmark source={content} />);
    }
    else if (contentType === "text/plain") {
      return (content);
    }
    else {
      return (<img src={`data:${contentType},${content}`} />)
    }
  }

  const checkComment = (val) => {
    if (val.contentType === "text/markdown") {
      return (<ListItemText primary={<ReactCommonmark source={val.comment} />} secondary={val.author.displayName} />);
    }
    else if (val.contentType === "text/plain") {
      return (<ListItemText primary={val.comment} secondary={val.author.displayName} />);
    }
    else {
      return (
        <Fragment>
          <ImageListItem><img src={`data:${val.contentType},${val.comment}`} /></ImageListItem>
          <ImageListItemBar position="below" title={val.author.displayName} />
        </Fragment>
      )
    }
  }

  const hiddenFileInput = React.useRef(null);

  const handleFileClick = event => {
    hiddenFileInput.current.click();
  };

  const handleFileUpload = event => {
    const fileUploaded = event.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(fileUploaded);

    reader.onload = () => {
      var base64result = reader.result.split(',')[1];
      setNewComment(base64result);
    };

  };

  return (
    <div className="Post">
      <Card className="Card" variant="outlined">
        <CardHeader
          style={{ textAlign: 'left' }}
          avatar={
            checkProfileImage()
          }
          title={title}
          subheader={name}
        />

        { }
        <CardContent>
          <Typography variant="body2" color="text.primary">
            <h3 className="Subtitles">Description</h3>
            {description}
          </Typography>
          <Typography variant="body2" color="text.primary">
            <h3 className="Subtitles">Content</h3>
            {checkContent()}
          </Typography>
        </CardContent>

        <CardActions className="CardActions">
          {/* <IconButton aria-label="like" onClick={handleLike}> */}
          {displayLike(id, "post.")}
          {/* </IconButton> */}
          <IconButton aria-label="comment" onClick={handleClickOpenCommentDialog}>
            <ChatBubbleOutlineIcon />
          </IconButton>
          <IconButton aria-label="share" onClick={handleClickOpenShareDialog}>
            <ShareIcon />
          </IconButton>
          {checkFromProfile()}
        </CardActions>
      </Card>

      {/* Dialog for comments */}
      <Dialog
        open={openCommentDialog}
        onClose={handleCloseCommentDialog}
        scroll="paper"
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Comments on {name}'s post</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {commentsForPost && commentsForPost.length > 0 && commentsForPost.map((val) => (
              <div key={val.id}>
                <ListItem
                  key={val.id}
                  disableGutters
                >
                  {checkComment(val)}
                  {/* <IconButton aria-label="like" onClick={handleLike}>
                    {displayLike(val.id)}
                  </IconButton> */}
                  {displayLike(val.id, "comment.")}
                </ListItem>
                <Divider />
              </div>
            ))}
          </DialogContentText>
          <div className="formElement">
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Choose Comment Type</InputLabel>
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
            {inputType === "image/png;base64" || inputType === "image/jpeg;base64" || inputType === "application/base64" ?
              <div className="UploadImage">
                <Button variant="contained" component="label" onClick={handleFileClick}>
                  Upload Image
                  <input type="file" ref={hiddenFileInput} onChange={handleFileUpload} hidden />
                </Button>
              </div>
              : ""
            }
          </div>
          <div className="formElement">
            {inputType === "text/plain" || inputType === "text/markdown" ?
              <TextField
                multiline
                autoFocus
                margin="dense"
                id="name"
                label="Add Comment"
                type="comment"
                fullWidth
                variant="standard"
                onChange={handleChangeComment}
                style={{ display: checkIfLoggedIn() }}
              />
              : ""
            }
          </div>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseCommentDialog}>Cancel</Button>
          <Button onClick={handleSubmitComments} style={{ display: checkIfLoggedIn() }}>Comment</Button>
        </DialogActions>

      </Dialog>

      {/* Dialog for sharing post */}
      <Dialog
        open={openShareDialog}
        onClose={handleCloseShareDialog}
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Share post to:</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {allAuthors.map((val) => (
              <div key={val.id}>
                <ListItem
                  key={val.id}
                  disableGutters
                  onClick={() => { SelectAuthor(val.id) }}
                  selected={val.id == authorToSend}
                >
                  <ListItemText primary={val.displayName} />
                </ListItem>
                <Divider />
              </div>
            ))}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseShareDialog}>Cancel</Button>
          <Button onClick={handleSharePost} style={{ display: checkIfLoggedIn() }}>Share</Button>
        </DialogActions>
      </Dialog>

      {/* Dialog for editing post */}
      <Dialog
        open={openEditDialog}
        onClose={handleCloseEditDialog}
        maxWidth='md'
        fullWidth={true}
      >
        <DialogTitle>Edit Post</DialogTitle>
        <DialogContent>
          <CreateNewPost
            id={id}
            name={name}
            user={user}
            author={author}
            title={title}
            description={description}
            contentType={contentType}
            content={content}
            img={img}
            visibility={visibility}
            newPost={false}
            closeDialog={handleCloseEditDialog}
          />
        </DialogContent>
        <DialogActions>
          {/* <Button onClick={handleCloseEditDialog}>Cancel</Button>
          <Button onClick={handleSubmitEdit}>Save</Button> */}
        </DialogActions>
      </Dialog>

      <Snackbar
        anchorOrigin={{ vertical, horizontal }}
        openCommentDialog={openSnackBar}
        autoHideDuration={6000}
        onClose={handleCloseSnackBar}
        key={vertical + horizontal}
      >
        <Alert severity="success" onClose={handleCloseSnackBar}>Comment Posted</Alert>
      </Snackbar>

    </div>
  );
}

export default Post;

Post.propTypes = {
  id: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  user: PropTypes.string.isRequired,
  author: PropTypes.object.isRequired,
  title: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  contentType: PropTypes.string.isRequired,
  content: PropTypes.string.isRequired,
  img: PropTypes.string,
  from: PropTypes.string.isRequired,
  commentsURL: PropTypes.string.isRequired,
  visibility: PropTypes.string.isRequired,
  reloadPosts: PropTypes.func.isRequired,
  post: PropTypes.object.isRequired,
}