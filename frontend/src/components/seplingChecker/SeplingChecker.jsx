import React, { useState } from "react";
import "./SeplingChecker.css";

function SpellingChecker() {
  const [word, setWord] = useState("");
  const [suggestions, setSuggestions] = useState("");

  const handleCheck = async () => {
    try {
      const response = await fetch("http://localhost:5000/spellcheck", {
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
      setSuggestions("Error fetching suggestions.");
    }
  };

  return (
    <div className="spellChecker">
      <h1>Spelling Checker</h1>
      <input
        type="text"
        placeholder="Enter the word"
        value={word}
        onChange={(e) => setWord(e.target.value)}
      />
      <button onClick={handleCheck}>Check</button>
      <p>Suggestions: {suggestions}</p>
    </div>
  );
}

export default SpellingChecker;
