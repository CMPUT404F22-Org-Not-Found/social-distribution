import React from "react";
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material";
import DynamicFeedIcon from '@mui/icons-material/DynamicFeed';
import PersonAddAltIcon from '@mui/icons-material/PersonAddAlt';
import AddIcon from '@mui/icons-material/Add';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

import './Topbar.css';

function Topbar() {

  // CHANGE ICON COLORS TO WHITE

  return (
    <div className="TopBar">
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <IconButton className="IconButton">
              <DynamicFeedIcon />

            </IconButton>

            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Social Distribution
            </Typography>

            <IconButton className="IconButton">
              <PersonAddAltIcon />
            </IconButton>

            <IconButton className="IconButton">
              <AddIcon />
            </IconButton>

            <IconButton className="IconButton">
              <NotificationsActiveIcon />
            </IconButton>

            <IconButton className="IconButton">
              <AccountCircleIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
      </Box>
    </div >
  );
}

export default Topbar;
