import React from "react";
import { useNavigate } from 'react-router-dom';
import { AppBar, Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, IconButton, Toolbar, Typography } from "@mui/material";
import DynamicFeedIcon from '@mui/icons-material/DynamicFeed';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import AddIcon from '@mui/icons-material/Add';
import InboxIcon from '@mui/icons-material/Inbox';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

import './Topbar.css';
import { useState } from "react";
import CreateNewPost from "./CreateNewPost";

function Topbar() {

  // CHANGE ICON COLORS TO WHITE
  // const navigate = useNavigate();
  // const navigateToLink = (link) => {
  //   navigate(link);
  // }

  const [openCreateDialog, setOpenCreateDialog] = useState(false);

  const navigate = useNavigate();
  const onClickFriendRequests = () => {
    navigate('/friend-requests');
  }

  const onClickHome = () => {
    navigate('/public-stream');
  }

  const onClickCreateNewPost = () => {
    navigate('/new-post');
  }

  const onClickNotifications = () => {
    navigate('/inbox');
  }

  const onClickProfile = () => {
    navigate('/profile');
  }

  const onClickLogin = () => {
    navigate('/login');
  }

  // HANDLE EDIT DIALOG
  const handleOpenCreateDialog = () => {
    setOpenCreateDialog(true);
  };

  const handleCloseCreateDialog = () => {
    setOpenCreateDialog(false);
  };

  return (
    <div className="TopBar">
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar className="Toolbar">
            <div>
              <IconButton className="IconButton" onClick={onClickHome}>
                <DynamicFeedIcon htmlColor="white" />
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: 'white' }}>
                  Social Distribution
                </Typography>
              </IconButton>
            </div>

            <div>
              <Button className="IconButton" onClick={onClickLogin}>
                Login
              </Button>

              <IconButton className="IconButton" onClick={onClickFriendRequests}>
                <PersonAddAltIcon htmlColor="white" />
              </IconButton>

              <IconButton className="IconButton" onClick={handleOpenCreateDialog}>
                <AddIcon htmlColor="white" />
              </IconButton>

              <IconButton className="IconButton" onClick={onClickNotifications}>
                <InboxIcon htmlColor="white" />
              </IconButton>

              <IconButton className="IconButton" onClick={onClickProfile}>
                <AccountCircleIcon htmlColor="white" />
              </IconButton>
            </div>
          </Toolbar>


          {/* Dialog for editing post */}
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
                author={""}
                title=""
                description=""
                contentType=""
                content=""
                img=""
                visibility=""
                newPost={true}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseCreateDialog}>Cancel</Button>
              <Button onClick={handleCloseCreateDialog}>Save</Button>
            </DialogActions>
          </Dialog>
        </AppBar>
      </Box>
    </div >
  );
}

export default Topbar;
