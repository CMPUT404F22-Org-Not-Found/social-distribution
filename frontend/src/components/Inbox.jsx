import React from "react";
import './Inbox.css';
import Post from "./Post";
// import Topbar from "./Topbar";
// import FriendRequests from "./FriendRequests";

function Inbox() {
  const samplePosts = [
    {
      name: 'Urvi Patel',
      user: 'urvipatel12',
      content: 'This is my first post on this app. So cool!',
      img: 'null',
      alt: 'null',
      date: 'September 10, 2022',
    },
    {
      name: 'Adit Rada',
      user: 'aditr',
      content: 'This app is just like twitter.',
      img: 'null',
      alt: 'null',
      date: 'Oct 22, 2022',
    },
    {
      name: 'Sanjeev Kotha',
      user: 'skotha',
      content: 'Look at this new recipe I made!',
      img: 'https://images.unsplash.com/photo-1627308595229-7830a5c91f9f',
      alt: 'Snacks',
      date: 'Oct 10, 2022',
    },
  ]

  const sampleComments = [
    {
      user: 'aditr',
      comment: 'Welcome to the app. Adding extra words to check width.',
    },
    {
      user: 'skotha',
      comment: 'I love twitter.',
    }
  ]

  return (
    <div className="Inbox">
      <h1>Inbox</h1>
       {samplePosts.map((val) => (
            <Post 
            name={val.name}
            user={val.user}
            content={val.content}
            img={val.img}
            alt={val.alt}
            date={val.date}
            fromProfile={false}
            comments={sampleComments}
            />
          ))}
    </div >
  );
}

export default Inbox;