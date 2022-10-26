import React from "react";
import { useNavigate } from 'react-router-dom';
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material";
import DynamicFeedIcon from '@mui/icons-material/DynamicFeed';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import AddIcon from '@mui/icons-material/Add';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

import './Topbar.css';

function Topbar() {

  // CHANGE ICON COLORS TO WHITE
  // const navigate = useNavigate();
  // const navigateToLink = (link) => {
  //   navigate(link);
  // }

  const navigate = useNavigate();
  const onClickFriendRequests = () => {
    navigate('/friend-requests');
  }

  const onClickHome = () => {
    navigate('/inbox');
  }

  const onClickCreateNewPost = () => {
    navigate('/new-post');
  }

  const onClickNotifications = () => {
    navigate('/notifications');
  }

  const onClickProfile = () => {
    navigate('/profile');
  }

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
              <IconButton className="IconButton" onClick={onClickFriendRequests}>
                <PersonAddAltIcon htmlColor="white"/>
              </IconButton>

              <IconButton className="IconButton" onClick={onClickCreateNewPost}>
                <AddIcon htmlColor="white" />
              </IconButton>

              <IconButton className="IconButton" onClick={onClickNotifications}>
                <NotificationsActiveIcon htmlColor="white" />
              </IconButton>

              <IconButton className="IconButton" onClick={onClickProfile}>
                <AccountCircleIcon htmlColor="white" />
              </IconButton>
            </div>
          </Toolbar>
        </AppBar>
      </Box>
    </div >
  );
}

export default Topbar;
