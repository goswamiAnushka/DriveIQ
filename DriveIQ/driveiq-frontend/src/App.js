import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import JourneyPage from './pages/JourneyPage';
import HistoryPage from './pages/HistoryPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './assets/styles.css';  // Add your global styles here

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/journey" element={<JourneyPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
