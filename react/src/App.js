import React, { useState, useEffect, useCallback } from 'react';
import useToken from './components/useToken'
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const [newDeadline, setNewDeadline] = useState("");
  const [images, setImages] = useState([]);
  const [showRegister, setShowRegister] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || null);


  const fetchTasks = useCallback(async () => {
    // if (!token) {
    //   console.error("No token available");
    //   return;
    // }
    
    console.log("Fetching tasks with token:", token);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/tasks', {
        method: 'GET',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
  
      if (response.ok) {
        const data = await response.json();
        console.log("Fetched tasks:", data);
        setTasks(data.tasks || []);
      } else {
        console.error("Failed to fetch tasks, status:", response.status);
      }
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  }, [token]);  

  

  useEffect(() => {
    if (token) {
      setIsLoggedIn(true);
      fetchTasks();
    }
  }, [token, fetchTasks]);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        alert("Registration successful! Please log in.");
        setShowRegister(false); 
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Registration failed. Try again.");
      }
    } catch (error) {
      setError("Error connecting to server.");
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
  
    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
  
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.token);
        setToken(data.token);
        setIsLoggedIn(true);
        fetchTasks();
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Invalid credentials. Please try again.");
      }
    } catch (error) {
      setError("Error logging in. Please try again later.");
    }
  };
  

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setTasks([]);
  };

  const handleTaskSubmission = async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('content', newTask);
    formData.append('date', newDeadline);
    images.forEach(image => formData.append('image', image));
  
    try {
      const response = await fetch('http://127.0.0.1:5000/tasks', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });
  
      if (response.ok) {
        const newTask = await response.json();
        setTasks([...tasks, newTask]);
        setNewTask("");
        setNewDeadline("");
        setImages([]);
      } else {
        console.error("Error adding task.");
      }
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };
  

  const handleDeleteTask = async (taskId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/tasks/${taskId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId));
      } else {
        console.error("Error deleting task");
      }
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  if (!isLoggedIn && !token) {
    return (
      <div className="App">
        <header className="App-header">
          {showRegister ? (
            <div>
              <h2>Register</h2>
              {error && <p style={{ color: "red" }}>{error}</p>}
              <form onSubmit={handleRegister}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="submit">Register</button>
              </form>
              <p>
                Already have an account?{" "}
                <button onClick={() => setShowRegister(false)}>Login</button>
              </p>
            </div>
          ) : (
            <div>
              <h2>Login to Task Manager</h2>
              {error && <p style={{ color: "red" }}>{error}</p>}
              <form onSubmit={handleLogin}>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button type="submit">Login</button>
              </form>
              <p>
                Don't have an account?{" "}
                <button onClick={() => setShowRegister(true)}>Register</button>
              </p>
            </div>
          )}
        </header>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Task Manager</h1>
        <button onClick={handleLogout}>Logout</button>

        <form onSubmit={handleTaskSubmission}>
          <input
            type="text"
            placeholder="Enter task content"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            required
          />
          <input
            type="date"
            value={newDeadline}
            onChange={(e) => setNewDeadline(e.target.value)}
            required
          />
          <input
            type="file"
            multiple
            onChange={(e) => setImages([...e.target.files])}
          />
          <button type="submit">Add Task</button>
        </form>

        <ul>
          {tasks.map(task => (
            <li key={task.id}>
              <h3>{task.content}</h3>
              <p>Deadline: {task.date}</p>
              <div>
                {task.images && task.images.map((img, idx) => (
                  <img
                    key={idx}
                    src={`data:image/jpeg;base64,${img}`}
                    alt="Task"
                    style={{ width: '100px', margin: '5px' }}
                  />
                ))}
              </div>
              <button onClick={() => handleDeleteTask(task.id)}>Delete Task</button>
            </li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
