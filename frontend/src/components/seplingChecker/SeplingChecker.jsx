import React, { useState } from "react";
import "./SeplingChecker.css";
import { Link } from "react-router-dom";

function SpellingChecker() {
  const [word, setWord] = useState("");
  const [suggestions, setSuggestions] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCheck = async () => {
    if (!word.trim()) {
      setError("Please enter a word to check");
      return;
    }

    setIsLoading(true);
    setError("");
    setSuggestions("");

    try {
      const response = await fetch("http://localhost:8080/spellcheck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ word }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setSuggestions(data.suggestions.join(", "));
    } catch (error) {
      console.error("Failed to fetch:", error);
      setError("Failed to get suggestions. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleCheck();
    }
  };

  return (
    <div className="spelling-checker">
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>
      
      <div className="checker-container">
        <Link to="/" className="back-button">
          ← Back to Home
        </Link>
        
        <div className="checker-content">
          <h1 className="checker-title">Sinhala Spelling Checker</h1>
          
          <div className="input-section">
            <div className="input-wrapper">
              <input
                type="text"
                placeholder="Enter Sinhala word to check..."
                value={word}
                onChange={(e) => setWord(e.target.value)}
                onKeyPress={handleKeyPress}
                className="word-input"
              />
              <button 
                onClick={handleCheck} 
                className="check-button"
                disabled={isLoading}
              >
                {isLoading ? "Checking..." : "Check Spelling"}
              </button>
            </div>
            
            {error && <div className="error-message">{error}</div>}
          </div>

          {suggestions && (
            <div className="results-section">
              <h2 className="results-title">Suggestions</h2>
              <div className="suggestions-container">
                {suggestions.split(", ").map((suggestion, index) => (
                  <div key={index} className="suggestion-item">
                    {suggestion}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SpellingChecker;
