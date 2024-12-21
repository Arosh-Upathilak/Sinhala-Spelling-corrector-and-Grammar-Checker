import React, { useState } from "react";
import "./GrammerChecker.css";

const GrammarChecker = () => {
  const [paragraph, setParagraph] = useState("");
  const [spellingCorrection, setSpellingCorrection] = useState("");
  const [grammarCorrection, setGrammarCorrection] = useState("");

  const handleCheck = async () => {
    const response = await fetch("http://localhost:5000/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paragraph }),
    });
    const data = await response.json();
    setSpellingCorrection(data.spelling_correction);
    setGrammarCorrection(data.grammar_correction);
  };

  return (
    <div className="grammar-checker">
      <h1>Grammar Checker</h1>
      <label>Enter the Paragraph:</label>
      <textarea
        value={paragraph}
        onChange={(e) => setParagraph(e.target.value)}
        placeholder="Enter Sinhala paragraph..."
      />
      <button onClick={handleCheck}>Check</button>
      <div className="suggestions">
        <h3>Suggestions:</h3>
        <p><strong>Spelling correction:</strong></p>
        <textarea value={spellingCorrection} readOnly />
        <p><strong>Grammar correction:</strong></p>
        <textarea value={grammarCorrection} readOnly />
      </div>
    </div>
  );
};

export default GrammarChecker;
