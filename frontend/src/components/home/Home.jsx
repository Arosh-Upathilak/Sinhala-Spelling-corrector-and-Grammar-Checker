import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>
      <div className="home-container">
        <h1 className="home-title">
          Sinhala Spell Checker And Grammar Checker
        </h1>
        <div className="home-content">
          <p className="options-label">Select your option</p>
          <div className="options-list">
            <Link to="/spellingChecker" className="option-link">
              <div className="option-card">
                <div className="option-icon">
                  <span className="option-number">01</span>
                </div>
                <div className="option-info">
                  <h2 className="option-title">Spelling Checker</h2>
                  <p className="option-description">Check and correct spelling errors in Sinhala text</p>
                </div>
              </div>
            </Link>
            <Link to="/grammarChecker" className="option-link">
              <div className="option-card">
                <div className="option-icon">
                  <span className="option-number">02</span>
                </div>
                <div className="option-info">
                  <h2 className="option-title">Grammar Checker</h2>
                  <p className="option-description">Analyze and improve Sinhala grammar</p>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;