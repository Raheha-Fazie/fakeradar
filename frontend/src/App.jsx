import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [verdictFilter, setVerdictFilter] = useState("All");
  const [deletingId, setDeletingId] = useState(null);

  // ============================================================
  // LOAD ANALYSIS HISTORY
  // ============================================================

  const loadClaims = async () => {
    try {
      const response = await fetch(`${API_URL}/claims`);

      if (!response.ok) {
        throw new Error("Failed to load analysis history");
      }

      const data = await response.json();

      setClaims(data.claims || []);
    } catch (error) {
      console.error("Error loading analysis history:", error);
    }
  };

  // ============================================================
  // LOAD HISTORY WHEN PAGE OPENS
  // ============================================================

  useEffect(() => {
    loadClaims();
  }, []);

  // ============================================================
  // ANALYZE NEWS
  // ============================================================

  const analyzeNews = async () => {
    const cleanText = text.trim();

    if (!cleanText) {
      alert("Please enter a news article first.");
      return;
    }

    if (cleanText.length < 20) {
      alert("Please enter a longer news article.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: cleanText,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Analysis failed");
      }

      setResult(data);

      // Refresh analysis history and statistics
      await loadClaims();
    } catch (error) {
      console.error("Analysis error:", error);

      alert(
        error.message ||
          "Backend connection failed. Make sure your Flask server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // ============================================================
  // DELETE ANALYSIS
  // ============================================================

  const deleteClaim = async (claimId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this analysis?"
    );

    if (!confirmed) {
      return;
    }

    setDeletingId(claimId);

    try {
      const response = await fetch(
        `${API_URL}/claims/${claimId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Failed to delete analysis"
        );
      }

      // Remove deleted analysis immediately
      setClaims((previousClaims) =>
        previousClaims.filter(
          (claim) => claim.id !== claimId
        )
      );
    } catch (error) {
      console.error("Delete error:", error);

      alert(
        error.message ||
          "Could not delete the analysis."
      );
    } finally {
      setDeletingId(null);
    }
  };

  // ============================================================
  // FORMAT DATE
  // ============================================================

  const formatDateTime = (timestamp) => {
    if (!timestamp) {
      return "Unknown";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
      return "Unknown";
    }

    return date.toLocaleString();
  };

  // ============================================================
  // ANALYSIS STATISTICS
  // ============================================================

  const statistics = useMemo(() => {
    const total = claims.length;

    const fake = claims.filter(
      (claim) =>
        String(claim.verdict || "")
          .toLowerCase() === "fake"
    ).length;

    const real = claims.filter(
      (claim) =>
        String(claim.verdict || "")
          .toLowerCase() === "real"
    ).length;

    const uncertain = claims.filter(
      (claim) =>
        String(claim.verdict || "")
          .toLowerCase() === "uncertain"
    ).length;

    return {
      total,
      fake,
      real,
      uncertain,
    };
  }, [claims]);

  // ============================================================
  // SEARCH + FILTER
  // ============================================================

  const filteredClaims = useMemo(() => {
    const normalizedSearch = searchTerm
      .trim()
      .toLowerCase();

    const normalizedVerdict = verdictFilter
      .trim()
      .toLowerCase();

    return claims
      .slice()
      .reverse()
      .filter((claim) => {
        const matchesSearch =
          !normalizedSearch ||
          String(claim.text || "")
            .toLowerCase()
            .includes(normalizedSearch);

        const matchesVerdict =
          verdictFilter === "All" ||
          String(claim.verdict || "")
            .toLowerCase() === normalizedVerdict;

        return matchesSearch && matchesVerdict;
      });
  }, [
    claims,
    searchTerm,
    verdictFilter,
  ]);

  // ============================================================
  // PERCENTAGE CALCULATIONS
  // ============================================================

  const fakePercentage =
    statistics.total > 0
      ? (statistics.fake / statistics.total) * 100
      : 0;

  const realPercentage =
    statistics.total > 0
      ? (statistics.real / statistics.total) * 100
      : 0;

  const uncertainPercentage =
    statistics.total > 0
      ? (statistics.uncertain / statistics.total) * 100
      : 0;

  // ============================================================
  // REFRESH ANALYSIS DATA
  // ============================================================

  const refreshStatistics = async () => {
    await loadClaims();
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div className="app-container">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="header">
        <h1>FakeRadar</h1>

        <p>
          AI-Powered Fake News Detection System
        </p>
      </header>


      {/* ======================================================
          YOUR ANALYSIS OVERVIEW
      ====================================================== */}

      <section className="dashboard-section">

        <div className="dashboard-header">

          <div>
            <h2>Your Analysis Overview</h2>

            <p className="section-description">
              View a summary of the news articles you have analyzed.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={refreshStatistics}
          >
            Refresh
          </button>

        </div>


        {/* ====================================================
            STATISTICS CARDS
        ==================================================== */}

        <div className="statistics-grid">

          {/* TOTAL ANALYSES */}

          <div className="stat-card total-card">

            <div className="stat-icon">
              📊
            </div>

            <div>
              <span className="stat-label">
                Total Analyses
              </span>

              <strong className="stat-number">
                {statistics.total}
              </strong>
            </div>

          </div>


          {/* FAKE NEWS */}

          <div className="stat-card fake-card">

            <div className="stat-icon">
              ⚠️
            </div>

            <div>
              <span className="stat-label">
                Fake News Detected
              </span>

              <strong className="stat-number">
                {statistics.fake}
              </strong>
            </div>

          </div>


          {/* REAL NEWS */}

          <div className="stat-card real-card">

            <div className="stat-icon">
              ✓
            </div>

            <div>
              <span className="stat-label">
                Real News Detected
              </span>

              <strong className="stat-number">
                {statistics.real}
              </strong>
            </div>

          </div>


          {/* UNCERTAIN */}

          <div className="stat-card uncertain-card">

            <div className="stat-icon">
              ?
            </div>

            <div>
              <span className="stat-label">
                Uncertain Results
              </span>

              <strong className="stat-number">
                {statistics.uncertain}
              </strong>
            </div>

          </div>

        </div>


        {/* ====================================================
            ANALYSIS DISTRIBUTION
        ==================================================== */}

        <div className="distribution-section">

          <h3>
            Analysis Distribution
          </h3>

          <div className="distribution-row">

            <span>
              Fake
            </span>

            <strong>
              {statistics.fake}
            </strong>

          </div>


          <div className="distribution-row">

            <span>
              Real
            </span>

            <strong>
              {statistics.real}
            </strong>

          </div>


          <div className="distribution-row">

            <span>
              Uncertain
            </span>

            <strong>
              {statistics.uncertain}
            </strong>

          </div>

        </div>


        {/* ====================================================
            VISUAL ANALYSIS DISTRIBUTION
        ==================================================== */}

        <div className="chart-section">

          <h3>
            Analysis Distribution
          </h3>

          <p className="chart-description">
            Percentage of your analyzed news articles by result.
          </p>


          {/* FAKE BAR */}

          <div className="chart-row">

            <div className="chart-label">

              <span>
                Fake
              </span>

              <strong>
                {statistics.fake} (
                {fakePercentage.toFixed(1)}%)
              </strong>

            </div>

            <div className="chart-bar-background">

              <div
                className="chart-bar fake-bar"
                style={{
                  width: `${fakePercentage}%`,
                }}
              />

            </div>

          </div>


          {/* REAL BAR */}

          <div className="chart-row">

            <div className="chart-label">

              <span>
                Real
              </span>

              <strong>
                {statistics.real} (
                {realPercentage.toFixed(1)}%)
              </strong>

            </div>

            <div className="chart-bar-background">

              <div
                className="chart-bar real-bar"
                style={{
                  width: `${realPercentage}%`,
                }}
              />

            </div>

          </div>


          {/* UNCERTAIN BAR */}

          <div className="chart-row">

            <div className="chart-label">

              <span>
                Uncertain
              </span>

              <strong>
                {statistics.uncertain} (
                {uncertainPercentage.toFixed(1)}%)
              </strong>

            </div>

            <div className="chart-bar-background">

              <div
                className="chart-bar uncertain-bar"
                style={{
                  width: `${uncertainPercentage}%`,
                }}
              />

            </div>

          </div>

        </div>

      </section>


      {/* ======================================================
          NEWS ANALYZER
      ====================================================== */}

      <section className="analyzer-section">

        <h2>
          Analyze News
        </h2>

        <p className="section-description">
          Paste a news article below to check its credibility.
        </p>

        <textarea
          rows="10"
          placeholder="Paste a news article here..."
          value={text}
          onChange={(event) =>
            setText(event.target.value)
          }
        />

        <button
          className="analyze-button"
          onClick={analyzeNews}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze News"}
        </button>

      </section>


      {/* ======================================================
          CURRENT RESULT
      ====================================================== */}

      {result && (

        <section className="result-section">

          <h2>
            Analysis Result
          </h2>

          <div className="result-card">

            <div className="result-item">

              <strong>
                Verdict
              </strong>

              <span
                className={`result-verdict ${String(
                  result.verdict || ""
                ).toLowerCase()}`}
              >
                {result.verdict}
              </span>

            </div>


            <div className="result-item">

              <strong>
                Confidence
              </strong>

              <span>
                {Number(
                  result.confidence || 0
                ).toFixed(2)}
                %
              </span>

            </div>


            <div className="result-message">

              <strong>
                Message
              </strong>

              <p>
                {result.message}
              </p>

            </div>

          </div>

        </section>

      )}


      {/* ======================================================
          ANALYSIS HISTORY
      ====================================================== */}

      <section className="tracker-section">

        <div className="tracker-header">

          <div>

            <h2>
              Analysis History
            </h2>

            <p className="section-description">
              View and manage your previously analyzed news articles.
            </p>

          </div>

          <span className="claim-count">

            {claims.length}{" "}

            {claims.length === 1
              ? "Analysis"
              : "Analyses"}

          </span>

        </div>


        {/* ====================================================
            SEARCH AND FILTER
        ==================================================== */}

        <div className="tracker-controls">

          <input
            type="text"
            className="search-input"
            placeholder="Search analyses..."
            value={searchTerm}
            onChange={(event) =>
              setSearchTerm(event.target.value)
            }
          />

          <select
            className="verdict-filter"
            value={verdictFilter}
            onChange={(event) =>
              setVerdictFilter(event.target.value)
            }
          >

            <option value="All">
              All Results
            </option>

            <option value="Fake">
              Fake
            </option>

            <option value="Real">
              Real
            </option>

            <option value="Uncertain">
              Uncertain
            </option>

          </select>

        </div>


        {/* ====================================================
            EMPTY ANALYSIS HISTORY
        ==================================================== */}

        {claims.length === 0 ? (

          <div className="empty-tracker">

            <h3>
              No news analyzed yet
            </h3>

            <p>
              Your analyzed news articles will appear here.
            </p>

          </div>

        ) : filteredClaims.length === 0 ? (

          <div className="empty-tracker">

            <h3>
              No matching results
            </h3>

            <p>
              Try changing your search or result filter.
            </p>

          </div>

        ) : (

          <div className="claims-list">

            {filteredClaims.map((claim) => (

              <div
                className="claim-card"
                key={claim.id}
              >

                {/* ANALYSIS HEADER */}

                <div className="claim-card-header">

                  <span className="claim-id">
                    Analysis #{claim.id}
                  </span>

                  <span className="claim-date">

                    {formatDateTime(
                      claim.created_at
                    )}

                  </span>

                </div>


                {/* NEWS TEXT */}

                <div className="claim-text">

                  <h3>
                    News Article
                  </h3>

                  <p>
                    {claim.text}
                  </p>

                </div>


                {/* ANALYSIS DETAILS */}

                <div className="claim-details">

                  <div className="detail-box">

                    <span className="detail-label">
                      Result
                    </span>

                    <strong
                      className={`claim-verdict ${String(
                        claim.verdict || ""
                      ).toLowerCase()}`}
                    >
                      {claim.verdict}
                    </strong>

                  </div>


                  <div className="detail-box">

                    <span className="detail-label">
                      Confidence
                    </span>

                    <strong>

                      {Number(
                        claim.confidence || 0
                      ).toFixed(2)}

                      %

                    </strong>

                  </div>


                  <div className="detail-box">

                    <span className="detail-label">
                      Analyzed On
                    </span>

                    <strong>

                      {formatDateTime(
                        claim.created_at
                      )}

                    </strong>

                  </div>

                </div>


                {/* ANALYSIS MESSAGE */}

                {claim.message && (

                  <div className="claim-message">

                    <span className="detail-label">
                      Analysis Message
                    </span>

                    <p>
                      {claim.message}
                    </p>

                  </div>

                )}


                {/* DELETE */}

                <div className="claim-actions">

                  <button
                    className="delete-button"
                    onClick={() =>
                      deleteClaim(claim.id)
                    }
                    disabled={
                      deletingId === claim.id
                    }
                  >

                    {deletingId === claim.id
                      ? "Deleting..."
                      : "Delete Analysis"}

                  </button>

                </div>

              </div>

            ))}

          </div>

        )}

      </section>

    </div>
  );
}

export default App;