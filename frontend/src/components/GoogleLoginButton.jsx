import React from "react";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import axiosInstance from "../utils/axiosInstance";

function GoogleLoginButton() {
  const { login } = useAuth();

  const handleSuccess = async (credentialResponse) => {
    try {
      // Clear any old token before new login
      localStorage.removeItem('access');
      
      // Step 1: Call Google login endpoint
      const response = await axiosInstance.post("/google-login", {
        token: credentialResponse.credential
      });
      
      console.log("Google login response:", response.data);
      
      // Step 2: Store the access token immediately
      localStorage.setItem('access', response.data.access);
      
      // Step 3: Try to get user info with the new token
      try {
        const userResponse = await axiosInstance.get("/me");
        console.log("User data:", userResponse.data);
        login(userResponse.data, response.data.access);
      } catch (meError) {
        console.error("Failed to get user data:", meError);
        // Even if /me fails, we still have the token - try to proceed
        if (response.data.access) {
          // Create a basic user object from Google data
          const basicUser = {
            email: "user@example.com", // We don't have real data yet
            name: "User",
            picture: null
          };
          login(basicUser, response.data.access);
        } else {
          throw new Error("No access token received");
        }
      }
      
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed. Please try again.");
      // Clear any partial data
      localStorage.removeItem('access');
    }
  };

  return (
    <div className="google-login-container">
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={() => {
          console.log("Google Login Failed");
          alert("Google login failed. Please try again.");
        }}
        theme="filled_blue"
        size="large"
        text="continue_with"
        shape="rectangular"
      />
    </div>
  );
}

export default GoogleLoginButton;