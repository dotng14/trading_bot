import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LogIn from './LogIn';
import Home from './Home';

const App: React.FC = () => {
    return (
          <Routes>
            <Route path="/" element={<LogIn />} />
            <Route path="/home" element={<Home />} />
          </Routes>
      );
};

export default App;