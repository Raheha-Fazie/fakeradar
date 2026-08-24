import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const analyzeNews = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    }
  };

  return (
    <div className="container">
      <h1>📰 FakeRadar</h1>
      <h3>AI-Powered Fake News Detection System</h3>

      <textarea
        placeholder="Paste your news article here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={analyzeNews}>
        Analyze News
      </button>

      {result && (
        <div className="result-card">

          <h2>Analysis Result</h2>

          <p>
            <strong>Verdict:</strong> {result.verdict}
          </p>

          <p>
            <strong>Confidence:</strong> {result.confidence}%
          </p>

          <p>{result.message}</p>

          <h3>Detected Keywords</h3>

          {result.keywords_detected &&
result.keywords_detected.length > 0 ? (
  <ul>
    {result.keywords_detected.map((word, index) => (
      <li key={index}>{word}</li>
    ))}
  </ul>
) : (
  <p>No suspicious keywords detected.</p>
)}

        </div>
      )}
    </div>
  );
}

export default App;