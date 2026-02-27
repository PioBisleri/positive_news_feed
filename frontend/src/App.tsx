import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ArticlePage from './pages/Article';
import Saved from './pages/Saved';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-amber-50 font-sans">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/article/:id" element={<ArticlePage />} />
            <Route path="/saved" element={<Saved />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
};

export default App;
