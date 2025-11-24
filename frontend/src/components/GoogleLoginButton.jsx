import React from "react";
import { GoogleLogin, googleLogout } from "@react-oauth/google";
import axios from "axios";

function GoogleLoginButton({ setUser }) {
  return (
    <GoogleLogin
      onSuccess={async (credentialResponse) => {
        const token = credentialResponse.credential;

        const res = await axios.post(
          "/api/google-login",
          { token },
          { withCredentials: true }
        );
        const user = res.data;
        localStorage.setItem("access", user.access);
        setUser(user);

      }}
      onError={() => console.log("Login Failed")}
    />
  );
}

export default GoogleLoginButton;
