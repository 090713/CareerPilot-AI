// ======================================================
// Login.jsx
// Login page for CareerPilot AI
// Handles user authentication using FastAPI backend
// ======================================================

// React Hooks
import { useState } from "react";

// Used to navigate between pages after successful login
import { useNavigate } from "react-router-dom";

// Axios instance for calling backend APIs
import api from "../api/api";

// Material UI Components
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  Alert,
} from "@mui/material";

function Login() {

  // ======================================================
  // State Variables
  // ======================================================

  // Stores email entered by the user
  const [email, setEmail] = useState("");

  // Stores password entered by the user
  const [password, setPassword] = useState("");

  // Shows loading state while waiting for backend response
  const [loading, setLoading] = useState(false);

  // Stores login error message
  const [error, setError] = useState("");

  // Used to redirect user to another page
  const navigate = useNavigate();


  // ======================================================
  // Login Function
  // Sends login request to FastAPI backend
  // ======================================================

  const handleLogin = async () => {

    // Show loading animation
    setLoading(true);

    // Clear previous error message
    setError("");

    try {

      // Send email and password to backend
      const response = await api.post("/auth/login", {
        email: email,
        password: password,
      });

      // Save JWT token in browser storage
      // This token will be used for future authenticated API requests
      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      // Redirect user to Dashboard
      navigate("/dashboard");

    } catch (err) {

      // Display backend error message
      setError(
        err.response?.data?.detail ||
        "Login failed"
      );

    } finally {

      // Stop loading animation
      setLoading(false);

    }
  };


  // ======================================================
  // User Interface
  // ======================================================

  return (
    <Container maxWidth="sm">

      <Box
        sx={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >

        <Card
          sx={{
            width: "100%",
            p: 2,
            borderRadius: 3,
            boxShadow: 5,
          }}
        >

          <CardContent>

            {/* Project Title */}

            <Typography
              variant="h4"
              align="center"
              fontWeight="bold"
              gutterBottom
            >
              CareerPilot AI
            </Typography>

            {/* Subtitle */}

            <Typography
              variant="subtitle1"
              align="center"
              color="text.secondary"
              mb={3}
            >
              Sign in to continue
            </Typography>


            {/* Email Input */}

            <TextField
              fullWidth
              label="Email"
              type="email"
              margin="normal"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />


            {/* Password Input */}

            <TextField
              fullWidth
              label="Password"
              type="password"
              margin="normal"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />


            {/* Show login error */}

            {
              error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )
            }


            {/* Login Button */}

            <Button
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3 }}

              // Call login function when clicked
              onClick={handleLogin}

              // Disable button while login request is processing
              disabled={loading}
            >

              {/* Change button text while loading */}

              {loading ? "Logging in..." : "Login"}

            </Button>


            {/* Register Message */}

            <Typography
              align="center"
              sx={{ mt: 3 }}
            >
              Don't have an account?
            </Typography>

          </CardContent>

        </Card>

      </Box>

    </Container>
  );
}

export default Login;