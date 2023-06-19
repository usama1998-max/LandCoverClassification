import React, { useState } from "react";
import Navbar from "../Navbar";
import { MDBContainer, MDBRow, MDBCol, MDBInput } from "mdb-react-ui-kit";
import defaultImage from '../../assests/img/defaultImage.png'
import axios from 'axios';
import { Link } from "react-router-dom";
export default function Home() {


  const [image, setImage] = useState(null);
const [ msg , setMsg] = useState(null);
  const handleImageChange = (event) => {
    const file = event.target.files[0];
setSelectedFile(file)
    const imageURL = URL.createObjectURL(file);
    setImage(imageURL);
handleSubmit(event.target.files[0]);
  };
    const [selectedFile, setSelectedFile] = useState(null);
  const handleSubmit = (file) => {
    const formData = new FormData();
    formData.append("media", file);
    axios
      .post("http://localhost:8000/image-classify/", formData)
      .then((res) => {
        console.log(res);
       if (res.data.status !== "error") {
       setMsg(res.data.category);
       return;
       }
       setMsg(res.data.msg);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  return (
    <>
      <MDBContainer
        fluid
        className="p-4 background-radial-gradient "
        style={{ height: "100vh", overflowX: "hidden " }}
      >
    <nav
      className="container navbar navbar-expand-lg "
      style={{
        boxShadow: "none",
        outline: "none !important",
        border: "none",
      }}
    >
      <a className="navbar-brand pl-3 text-white navbarHeading" href="#">
      Image Classification 
      </a>
      <button
        className="navbar-toggler text-white"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>

      <div className="collapse navbar-collapse" id="navbarNavDropdown">
        <div className="navbar-nav ml-auto"> 
        <input type="text" className="search" alt="Search" placeholder="Search..." />
        </div>
        <div className="navbar-nav ml-auto"> 
       <Link to="/signin"><button type="button" className="btn btn btn-outline-secondary headerContract text-white">Login</button></Link>
       <Link to="/signup"><button  className='btn btn btn-dark ml-2 headerTryDante' >Sigin Up</button></Link>
        </div>
      </div>
    </nav>
        <div className="container">
          <h1 className="heading">Explore Best Places In City </h1>
          <h6 className="subHeading">Find some of the best tips from around the city from our partners and friends</h6>

        </div>
        <MDBRow className="image-input-container my-5">
        <MDBCol md={8} className="d-flex flex-column justify-content-center " >
  <label htmlFor="form3" className="btn btn-primary mx-auto" style={{width:"130px", }}>
    Select Image
    <input
      id="form3"
      type="file"
      onChange={handleImageChange}
      style={{ display: "none" }}
    />
  </label>
</MDBCol>
 <MDBCol
            md="12">
            <div style={{textAlign:"center", color: "green" , backgroundColor:"white"}}
            >
            <h1 style={{textAlign:"center", color: "black"}}>Result: {msg}</h1>
            </div>
            </MDBCol>
          <MDBCol
            md="6"
            className="image-preview-container text-center text-md-start d-flex flex-column justify-content-center"
          >
            {!image ? 
              <img src={defaultImage} className="img-fluid hover-shadow" alt="" />  : (

              
              <img src={image} className="img-fluid hover-shadow" alt="" />
            )}
          </MDBCol>
        </MDBRow>
        <footer className="bg-transparent text-white py-4">
          <div className="container">
            <div className="row text-center">
              <div className="col-md-4">
                <h5 className="text-white">About</h5>
                <ul className="list-unstyled">
                  <li>
                    <a href="#" className="text-white">
                      About Us
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      Our Team
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      History
                    </a>
                  </li>
                </ul>
              </div>
              <div className="col-md-4">
                <h5 className="text-white">Contact Us</h5>
                <ul className="list-unstyled">
                  <li>
                    <a href="#" className="text-white">
                      Contact Information
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      Customer Support
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      FAQ
                    </a>
                  </li>
                </ul>
              </div>
              <div className="col-md-4">
                <h5 className="text-white">Features</h5>
                <ul className="list-unstyled">
                  <li>
                    <a href="#" className="text-white">
                      Product Features
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      Pricing
                    </a>
                  </li>
                  <li>
                    <a href="#" className="text-white">
                      Blog
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="row mt-4">
              <div className="col-md-12 text-center">
                <p className="mb-0 text-white">
                  &copy; {new Date().getFullYear()} Your Company. All rights
                  reserved.
                </p>
              </div>
            </div>
          </div>
        </footer>
      </MDBContainer>
    </>
  );
}
