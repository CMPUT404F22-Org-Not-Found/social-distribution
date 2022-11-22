import './App.css';
import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Inbox from './components/Inbox';
import FriendRequests from './components/FriendRequests';
import Dashboard from './components/Dashboard';
import CreateNewPost from './components/CreateNewPost';
import Profile from './components/Profile';
import PublicStream from './components/PublicStream';
import Login from './components/Login';
import Register from './components/Register';

function App() {
  return (
    <div className="App">
      <p>Testing deployment</p>
      {/* <Routes>
        <Route path="" element={<Dashboard />}>
          <Route path="/" element={<Navigate replace to="/public-stream" />} />
          <Route path="/public-stream" element={<PublicStream />} />
          <Route path="/friend-requests" element={<FriendRequests />} />
          <Route path="/new-post" element={<CreateNewPost />} />
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes> */}
    </div>
  );
}

export default App;
