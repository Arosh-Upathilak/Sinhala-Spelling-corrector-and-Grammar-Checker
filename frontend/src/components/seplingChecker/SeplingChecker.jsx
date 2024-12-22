import React, { useState } from "react";
import "./SeplingChecker.css";
import { Link } from "react-router-dom";

function SpellingChecker() {
  const [sentence, setSentence] = useState("");
  const [correctedSentence, setCorrectedSentence] = useState("");
  const [suggestions, setSuggestions] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  // Keeping all original functions unchanged
  const handleCheck = async () => {
    if (!sentence.trim()) {
      setError("Please enter a sentence to check.");
      return;
    }

    setIsLoading(true);
    setError("");
    setCorrectedSentence("");
    setSuggestions("");

    try {
      const response = await fetch("http://localhost:8080/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setCorrectedSentence(data.spelling_correction);
      setSuggestions(data.errors);
    } catch (error) {
      console.error("Failed to fetch:", error);
      setError("Failed to get corrections. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(correctedSentence).then(() => {
      alert("Corrected sentence copied to clipboard!");
    });
  };

  const handleDownload = () => {
    const element = document.createElement("a");
    const file = new Blob([correctedSentence], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "corrected_sentence.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
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
            <label htmlFor="textInput" className="input-label">
              Enter your text:
            </label>
            <textarea
              id="textInput"
              placeholder="Enter Sinhala text to check grammar and spelling..."
              value={sentence}
              onChange={(e) => setSentence(e.target.value)}
              onKeyPress={handleKeyPress}
              className="text-input"
              rows={6}
            />
            <button 
              onClick={handleCheck} 
              className="check-button"
              disabled={isLoading}
            >
              {isLoading ? "Checking..." : "Check Text"}
            </button>

            {error && <div className="error-message">{error}</div>}
          </div>

          {suggestions && (
            <div className="results-section">
              <h2 className="results-title">Suggestions</h2>
              <div className="suggestions-container">
                {suggestions.split("\n").map((error, index) => (
                  <div key={index} className="suggestion-item">
                    {error}
                  </div>
                ))}
              </div>
            </div>
          )}

          {correctedSentence && (
            <div className="results-section">
              <h2 className="results-title">Corrected Spelling Text</h2>
              <div className="corrected-text">
                {correctedSentence}
              </div>
              <div className="action-buttons">
                <button className="action-button" onClick={handleCopy}>
                  Copy Text
                </button>
                <button className="action-button" onClick={handleDownload}>
                  Download Text
                </button>
              </div>
            </div>
          )}

          
        </div>
      </div>
    </div>
  );
}

export default SpellingChecker;
