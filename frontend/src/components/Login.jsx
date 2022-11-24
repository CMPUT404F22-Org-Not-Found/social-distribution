import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  TextField,
  Paper,
  Button
} from '@mui/material';
import axiosInstance from '../axiosInstance';
import { useState } from 'react';


function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleUsernameChange = (event) => {
      setUsername(event.target.value)
    }

    const handlePasswordChange = (event) => {
      setPassword(event.target.value)
    }

    const onClickLogin = () => {
      const params = {
        username,
        password,
      }
      const url = "/api-token-auth/"

      axiosInstance.post(url, params).then((response) => {
        console.log(response.data.token);
        window.localStorage.setItem("auth-token", response.data.token);
        navigate('/');
      })
    }

    const onClickRegister = () => {
        navigate('/register');
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
            <TextField label="Username" onChange={handleUsernameChange}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Password" type={'password'} onChange={handlePasswordChange}></TextField>
          </Grid>
          <Grid item xs={12}>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth onClick={onClickLogin}> Login </Button>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth onClick={onClickRegister}> Register </Button >
          </Grid>
        </Grid>
      </Paper>
    </div>
  );
};

export default Login;