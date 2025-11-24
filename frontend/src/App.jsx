import React, { useEffect, useState } from "react";
import GoogleLoginButton from "./components/GoogleLoginButton";
import axios from "axios";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
  const token = localStorage.getItem("access");
  if (!token) return;

  axios.get("/api/me", {
    headers: { Authorization: `Bearer ${token}` },
    withCredentials: true
  })
  .then(res => setUser(res.data))
  .catch(() => setUser(null));
  }, []);


  return (
    <div style={{ padding: 40 }}>
      <h1>Google Login - 15 Day Session</h1>

      {user ? (
        <>
          <h2>Welcome {user.email}</h2>
          <button
            onClick={() => {
              axios.post("/api/auth/logout", {}, { withCredentials: true });
              setUser(null);
            }}
          >
            Logout
          </button>
        </>
      ) : (
        <GoogleLoginButton setUser={setUser} />
      )}
    </div>
  );
}

export default App;
