import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
  TextField,
  Paper,
  Button
} from '@mui/material';

function Register() {

    const navigate = useNavigate();

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
            <TextField label="Username"></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Display Name"></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="GitHub URL"></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Password" type={'password'}></TextField>
          </Grid>
          <Grid item xs={12}>
            <TextField label="Confirm Password" type={'password'}></TextField>
          </Grid>
          <Grid item xs={12}>
          </Grid>
          <Grid item xs={6}>
            <Button fullWidth> Register </Button>
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