import React, { useState } from 'react';

const LogIn: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();

    if (data.success) {
      alert('Logged in successfully');
    } else if (data.message.includes('challenge')) {
      // Handle 2FA challenge
      const code = prompt('Enter 2FA code');
      if (code) {
        const challenge_id = data.challenge_id;
        const response = await fetch('http://127.0.0.1:5000/auth', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password, challenge_id, code }),
        });
        const mfaData = await response.json();

        if (mfaData.success) {
          alert('Logged in successfully');
        } else {
          alert(mfaData.message);
        }
      }
    } else {
      alert(data.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Log In</h2>
      <form onSubmit={(e) => { e.preventDefault(); handleLogin(); }}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Log In</button>
      </form>
    </div>
  );
};

export default LogIn;