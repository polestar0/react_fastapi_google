import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { GoogleOAuthProvider } from "@react-oauth/google";

ReactDOM.createRoot(document.getElementById("root")).render(
<GoogleOAuthProvider clientId="60209345033-dagb9pvr7maru9uq13i7ntoj4p513ls5.apps.googleusercontent.com">
  <App />
</GoogleOAuthProvider>

);