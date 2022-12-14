import './App.css';
import React, { useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Inbox from './components/Inbox';
import FriendRequest from './components/FriendRequest';
import Dashboard from './components/Dashboard';
import CreateNewPost from './components/CreateNewPost';
import Profile from './components/Profile';
import PublicStream from './components/PublicStream';
import Login from './components/Login';
import Register from './components/Register';
import RedirectIfLoggedIn from './RedirectIfLoggedIn';
import ProtectedRoute from './Protected';
import AuthorList from './components/AuthorList';

function App() {
  return (
    <div className="App">
      <Routes>

        <Route path="" element={<Dashboard />}>
          <Route path="/" element={<Navigate replace to="/public-stream" />} />
          <Route path="/public-stream" element={<PublicStream />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/author-list" element={<AuthorList />} />
            {/* <Route path="/friend-requests" element={<FriendRequests />} /> */}
            {/* <Route path="/new-post " element={<CreateNewPost />} /> */}
            <Route path="/inbox" element={<Inbox />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
        </Route>
        <Route element={<RedirectIfLoggedIn />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
