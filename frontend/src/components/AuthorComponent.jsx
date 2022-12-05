import { Avatar, Button, Card, CardActions, CardContent, IconButton, Typography, CardHeader } from "@mui/material";
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import PropTypes from 'prop-types';
import { deepOrange } from '@mui/material/colors';

import React, { useState, useEffect } from "react";
import './AuthorComponent.css';
import axios from "axios";
import axiosInstance from "../axiosInstance";

function AuthorComponent(props) {
    const { type, id, host, displayName, url, github, profileImage } = props

    const authorId = localStorage.getItem("authorId");
    const authorObject = JSON.parse(localStorage.getItem("author"));

    const showProfile = () => {

    }

    const addFriend = () => {
        console.log("friend request sent to" + { displayName })
        const postData = {
            type: "Follow",
            summary: authorObject.displayName + " sent you a friend request.",
            object: {
                type: type,
                id: id,
                host: host,
                displayName: displayName,
                url: url,
                github: github,
                profileImage: profileImage
            },
            actor: authorObject,
        };
        console.log("Make axios call to send a friend request.");

        // console.log("SPLIT ID:", id.split("/"))
        let postID = id.split("/").pop();

        // const URLtoParse = new URL(id)
        // if (URLtoParse.hostname === "cmput-404-team-1.herokuapp.com") {
        //     postID = postID.replace(/-/g, "");
        // }

        console.log("Final URL:", postID);

        const postUrl = "authors/" + postID + "/inbox/"
        console.log(postData)
        console.log(postUrl)
        axiosInstance.post(postUrl, postData)
            .then((response) => {
                console.log("friend request sent")
                console.log(response);
            })
    }

    return (
        <div className="Author">
            <Card
                className="Card"
                variant="outlined"
                onClick={showProfile}
            >
                <CardHeader
                    avatar={
                        <Avatar
                            sx={{ bgcolor: deepOrange[500] }}
                            alt={displayName}
                            src={profileImage}
                        />}
                    title={displayName}
                    subheader={
                        <a href={github}>Visit Github</a>
                    }
                    action={
                        <IconButton
                            aria-label="Add Friend"
                            onClick={addFriend}
                        >
                            <PersonAddAlt1Icon />
                        </IconButton>
                    }
                />
            </Card>
        </div>
    );
}

export default AuthorComponent;

AuthorComponent.propTypes = {
    type: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    host: PropTypes.string.isRequired,
    displayName: PropTypes.string.isRequired,
    url: PropTypes.string.isRequired,
    github: PropTypes.string.isRequired,
    profileImage: PropTypes.string.isRequired,
}