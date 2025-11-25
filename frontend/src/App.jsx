import React, { useState } from "react";
import { useAuth } from "./context/AuthContext";
import GoogleLoginButton from "./components/GoogleLoginButton";
import "./App.css";

function App() {
  const { user, loading, logout } = useAuth();
  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);

  const handleLogout = () => {
    logout();
  };

  const confirmLogout = () => {
    setShowLogoutConfirm(true);
  };

  const cancelLogout = () => {
    setShowLogoutConfirm(false);
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <p>Checking authentication...</p>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="app-container">
        <header className="app-header">
          <h1>Google Authentication</h1>
          <p>Secure 15-day session with automatic token refresh</p>
        </header>

        <main className="app-main">
          {user ? (
            <div className="user-dashboard">
              <div className="welcome-section">
                <div className="avatar">
                  {user.picture ? (
                    <img src={user.picture} alt={user.name} />
                  ) : (
                    <div className="avatar-placeholder">
                      {user.name?.charAt(0).toUpperCase()}
                    </div>
                  )}
                </div>
                <h2>Welcome back, {user.name}!</h2>
                <p className="user-email">{user.email}</p>
              </div>
              
              <div className="session-info">
                <p>Your session is active and will automatically refresh for up to 15 days.</p>
                <p className="session-detail">Access tokens refresh automatically when expired.</p>
              </div>

              <button 
                className="logout-btn"
                onClick={confirmLogout}
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div className="login-section">
              <div className="login-card">
                <h2>Sign in to continue</h2>
                <p>Please sign in with your Google account to access the application.</p>
                <GoogleLoginButton />
              </div>
            </div>
          )}
        </main>

        {/* Logout Confirmation Modal */}
        {showLogoutConfirm && (
          <div className="logout-confirm-modal">
            <div className="modal-content">
              <h3>Confirm Sign Out</h3>
              <p>Are you sure you want to sign out?</p>
              <div className="modal-actions">
                <button 
                  className="btn-secondary"
                  onClick={cancelLogout}
                >
                  Cancel
                </button>
                <button 
                  className="logout-btn"
                  onClick={handleLogout}
                >
                  Yes, Sign Out
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;