import logo from './logo.svg';
import './App.css';
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login'; // Make sure path is correct

function App() {
   return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* Add more routes like Register, Dashboard here */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
