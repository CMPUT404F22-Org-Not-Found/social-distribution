import axios from "axios";
import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import AuthorComponent from "./AuthorComponent";
import './AuthorList.css';

function AuthorList() {
  const [allAuthors, setAllAuthors] = useState([]);

  function getAuthorList() {
    // const baseURL = "http://localhost:8000/authors/"
    // axios.get(baseURL).then((response) => {
    //   setAllAuthorList(response.data.items);
    // });

    const baseURL = "http://localhost:8000/authors/"
    axios.get(baseURL).then((response) => {
      setAllAuthors(response.data.items);
    });
    console.log(allAuthors); 
  }

  useEffect(() => {
    getAuthorList();
    console.log(allAuthors);
  }, []);

  return (
    <div className="StreamOfAuthors">
      <h1>Author List</h1>
      {allAuthors.map((val) => (
        <AuthorComponent
          key={val.id}
          type={val.type}
          id={val.id}
          host={val.host}
          displayName={val.displayName}
          url={val.url}
          github={val.github}
          profileImage={val.profileImage}
        />
      ))}
    </div>
  );
}

export default AuthorList;