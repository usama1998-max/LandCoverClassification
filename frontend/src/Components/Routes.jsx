import React from "react";
import { Routes as Switch, Route  } from "react-router-dom";
import Login from "./Pages/Login";
import Register from "./Pages/Register";
import Home from "./Pages/Home";

export default function Routes() {
  return (
    <>
      <>
        <Switch>
          <Route path="/home" element={<Home />} />
          <Route path="/" element={<Login />} />
          <Route path="/signin" element={<Login />} />
          <Route path="/signup" element={<Register />} />
        </Switch>
      </>
    </>
  );
}
