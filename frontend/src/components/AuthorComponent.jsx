import { Avatar, Button, Card, CardActions, CardContent, IconButton, Typography, CardMedia } from "@mui/material";
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import PropTypes from 'prop-types';

import React, { useState, useEffect } from "react"; 
import './AuthorComponent.css';
import axios from "axios";
import axiosInstance from "../axiosInstance";

function AuthorComponent(props) {
    const {id, host, displayName, url, github, profileImage} = props

    return (
        <div className="Author">
            <Card 
            className="Card" 
            variant="outlined" 
            >
                <CardContent>
                    <CardMedia
                        component="img"
                        sx={{ width: 151 }}
                        image={profileImage}
                        alt={displayName[0]}
                    />
                    <Typography variant="h6" color="text.primary">
                        {displayName}
                        <a href={github}>Visit Github</a>
                    </Typography>
                </CardContent>

                <CardActions className="CardActions">
                    <IconButton aria-label="Add Friend">
                        <PersonAddAlt1Icon/>
                    </IconButton>  
                    <IconButton aria-label="Show Profile">
                        <ExpandMoreIcon/>
                    </IconButton>
                </CardActions>
            </Card>
        </div>
    );}

export default AuthorComponent;

AuthorComponent.propTypes = {
    id: PropTypes.string.isRequired,
    host: PropTypes.string.isRequired,
    displayName: PropTypes.string.isRequired,
    url: PropTypes.object.isRequired,
    github: PropTypes.string.isRequired,
    profileImage: PropTypes.string.isRequired,
}