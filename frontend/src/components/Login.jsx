import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  TextField,
  Paper,
  Button
} from '@mui/material';


function Login() {

    const navigate = useNavigate();
    
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
            <TextField label="Username"></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Password" type={'password'}></TextField>
          </Grid>
          <Grid item xs={12}>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth> Login </Button>
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