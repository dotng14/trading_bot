import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LogIn from './LogIn';
import Register from './Register';
import Home from './Home';
import BotAccount from './BotAccount';

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<BotAccount />} />
      <Route path="/bot_login" element={<BotAccount />} />
      <Route path="/login" element={<LogIn />} />
      <Route path="/register" element={<Register />} />
      <Route path="/home" element={<Home />} />
    </Routes>
  );
};

export default App;