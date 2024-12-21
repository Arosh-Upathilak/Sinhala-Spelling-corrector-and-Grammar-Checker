import React from 'react';
import './Home.css';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home">
      <h1> Sinhala Spell Checker And Grammar Checker </h1>
      <div>
        <p>Select your option:</p>
        <ul>
          <li><Link to="/spellingChecker">01. Spelling Checker</Link></li>
          <li><Link to="/grammarChecker">02. Grammar Checker</Link></li>
        </ul>
      </div>
    </div>
  );
}

export default Home;
