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
import axios from 'axios';


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
      // const url = "/api-token-auth/"
      const url = "https://cmput404-t04.herokuapp.com/author-object/"

      axios.post(url, params).then((response) => {
        console.log(response.data);
        localStorage.setItem("auth-token", response.data.token);
        navigate('/');
        console.log("Token from storage:", localStorage.getItem("auth-token"))

        // setAuthor(response.data.author);
        // console.log("Author:", Author);
        const id = response.data.author.id.split("/").pop()
        const author = response.data.author
        localStorage.setItem("author", JSON.stringify(author));
        localStorage.setItem("authorId", id);
        console.log("AuthorID from storage: ", localStorage.getItem("authorId"));
        console.log("Author from storage: ", JSON.parse(localStorage.getItem("author")));

      })
    }

    // const setAuthor = (input) => {
    //   Author.authorObject = input;
    //   Author.authorId = input.id.split("/").pop();
    // }

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