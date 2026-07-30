import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const analyzeNews = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text,
          }),
        }
      );

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    }
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>FakeRadar</h1>

      <textarea
        rows="8"
        cols="60"
        placeholder="Paste news article here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />
      <br />

      <button onClick={analyzeNews}>
        Analyze
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Result</h2>

          <p>
            <strong>Verdict:</strong>{" "}
            {result.verdict}
          </p>

          <p>
            <strong>Confidence:</strong>{" "}
            {result.confidence}%
          </p>

          <p>{result.message}</p>
        </div>
      )}
    </div>
  );
}

export default App;