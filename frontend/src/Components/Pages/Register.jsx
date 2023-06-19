import React , { useState} from "react";
import { enqueueSnackbar } from "notistack";
import axios from "axios";
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBCheckbox,
  MDBIcon,
} from "mdb-react-ui-kit";
import { Link } from "react-router-dom";

export default function Register() {
 const [loading, setLoading] = useState(false);
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
  });
  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://localhost:8000/register/", {username: loginData.email, password: loginData.password}, {
          headers: {
            "Content-Type": "application/json",
          },
        })
      .then((res) => {
        setLoading(false);
        console.log();
        if (res.data.status !== "error") {
          setLoginData({
            email: "",
            password: "",
          });
//           localStorage.setItem("token", res.data.token);
          enqueueSnackbar("Successfully Register.", {
            variant: "success",
          });
          window.location.href = "/home";
          // return redirect("/home");
          return;
        }
        console.log(res.data.msg);
         return enqueueSnackbar(res.data.msg, {
            variant: "error",
          });
      })
      .catch((err) => {
      console.log(err);

      });
  };
  return (
    <MDBContainer
      fluid
      className="p-4 background-radial-gradient "
      style={{ height: "100vh", overflowX: "hidden " }}
    >
    
      <MDBRow>
        <MDBCol
          md="6"
          className="text-center text-md-start d-flex flex-column justify-content-center"
        >
          <h1
            className="my-5 display-3 fw-bold ls-tight px-3"
            style={{ color: "hsl(218, 81%, 95%)" }}
          >
            The best offer <br />
            <span style={{ color: "hsl(218, 81%, 75%)" }}>
              for your business
            </span>
          </h1>

          <p className="px-3" style={{ color: "hsl(218, 81%, 85%)" }}>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Eveniet,
            itaque accusantium odio, soluta, corrupti aliquam quibusdam tempora
            at cupiditate quis eum maiores libero veritatis? Dicta facilis sint
            aliquid ipsum atque?
          </p>
        </MDBCol>

        <MDBCol md="6" className="position-relative">
          <div
            id="radius-shape-1"
            className="position-absolute rounded-circle shadow-5-strong"
          ></div>
          <div
            id="radius-shape-2"
            className="position-absolute shadow-5-strong"
          ></div>

          <MDBCard className="my-5 bg-glass">
            <MDBCardBody className="p-5">
              <MDBRow>
                <MDBCol
                  md="12"
                  className="text-center text-md-start d-flex   justify-content-center"
                >
                  <h1>Register</h1>
                </MDBCol>
              </MDBRow>
              <MDBRow>
                <MDBCol md={12}>
                  {" "}
                  <br />
                </MDBCol>
              </MDBRow>


              <MDBInput
                  wrapperClass="mb-4"
                  label="Email"
                  id="form3"
                  type="email"
                        value= {loginData.email}
      onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
                />
                <MDBInput
                  wrapperClass="mb-4"
                  label="Password"
                  id="form4"
                  type="password"
                   value= {loginData.password}
      onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                />




              <MDBBtn  onClick={handleSubmit} className="w-100 mb-4" size="md">
           sign up
              
              </MDBBtn>
            
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
  
    </MDBContainer>
  );
}
