import './App.css';
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import SpellingChecker from "./components/seplingChecker/SeplingChecker";
import GrammarChecker from "./components/grammerChecker/GrammerChecker";

function App() {
  return (
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/spellingChecker' element={<SpellingChecker />} />
        <Route path='/grammarChecker' element={<GrammarChecker />} />
      </Routes>
  );
}

export default App;
