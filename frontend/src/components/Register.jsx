import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  TextField,
  Paper,
  Button
} from '@mui/material';
import axiosInstance from '../axiosInstance.js';
import axios from 'axios';

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [github, setGithub] = useState("");
  const[profileImage, setProfileImage] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
    console.log(username);
  }

  const handleDisplayNameChange = (event) => {
    setDisplayName(event.target.value);
    console.log(displayName);

  }

  const handleGithubChange = (event) => {
    setGithub(event.target.value);
    console.log(github);

  }

  const handleProfileImageChange = (event) => {
    setProfileImage(event.target.value);
    console.log(profileImage);
  }

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
    console.log(password);

  }

  const handleConfirmPasswordChange = (event) => {
    setConfirmPassword(event.target.value);
    console.log(confirmPassword);

  }


  const onClickRegister = () => {
    const registerData = {
      username,
      displayName,
      github,
      profileImage,
      password1: password,
      password2: confirmPassword,
    }

    console.log(registerData);
    const url = "http://localhost:8000/register/"

    axios.post(url, registerData)
    .then((response) => {
      console.log(response)
      navigate('/login');
      });
  }

  const onClickLogin = () => {
    navigate('/login');
  }

  return (
    <div style={{ padding: 30 }}>
      <Paper>
        <Grid
          container
          spacing={3}
          direction={'column'}
          justify={'center'}
          alignItems={'center'}
        >
          <Grid item xs={12}>
            <TextField label="Username" onChange={handleUsernameChange} />
          </Grid>
          <Grid item xs={12}>
            <TextField label="Display Name" onChange={handleDisplayNameChange}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="GitHub URL" onChange={handleGithubChange}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Profile Image" onChange={handleProfileImageChange}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Password" type={'password'} onChange={handlePasswordChange}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Confirm Password" type={'password'} onChange={handleConfirmPasswordChange}></TextField>
          </Grid>
          <Grid item xs={12}>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth onClick={onClickRegister}> Register</Button>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth onClick={onClickLogin}> Login </Button>
          </Grid>
        </Grid>
      </Paper>
    </div>
  );

};

export default Register;