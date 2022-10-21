import React from "react";
import Post from "./Post";
import Topbar from "./Topbar";

import './Inbox.css';

function Inbox() {
  return (
    <div className="Inbox">
      <Topbar />
      <div className="Posts">
        <Post />
      </div>
    </div>
  );
}

export default Inbox;