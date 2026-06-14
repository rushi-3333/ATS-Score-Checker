import ResumeTips from "./ResumeTips";
import "./ScoreCard.css";

const CATEGORY_LABELS = {
  format_structure: "Format & Structure",
  keywords_skills: "Keywords & Skills",
  experience: "Experience",
  contact_education: "Contact & Education",
};

function getScoreColor(score) {
  if (score >= 80) return "#22c55e";
  if (score >= 60) return "#eab308";
  if (score >= 40) return "#f97316";
  return "#ef4444";
}

function ScoreCard({ result, fileName }) {
  const { overall_score, categories, strengths, improvements, summary } = result;

  return (
    <div className="score-card">
      <div className="score-header">
        <div>
          <h2>ATS Analysis Results</h2>
          <span className="file-name">{fileName}</span>
        </div>
        <div className="overall-score" style={{ borderColor: getScoreColor(overall_score) }}>
          <span className="score-value" style={{ color: getScoreColor(overall_score) }}>
            {overall_score}
          </span>
          <span className="score-label">Overall Score</span>
        </div>
      </div>

      <p className="summary">{summary}</p>

      <div className="categories-grid">
        {Object.entries(categories || {}).map(([key, cat]) => (
          <div key={key} className="category-card">
            <div className="category-header">
              <span>{CATEGORY_LABELS[key] || key}</span>
              <strong style={{ color: getScoreColor(cat.score) }}>{cat.score}</strong>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${cat.score}%`,
                  backgroundColor: getScoreColor(cat.score),
                }}
              />
            </div>
            <p className="category-feedback">{cat.feedback}</p>
          </div>
        ))}
      </div>

      <div className="lists-section">
        <div className="list-card strengths">
          <h3>Strengths</h3>
          <ul>
            {(strengths || []).map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="list-card improvements">
          <h3>Improvements</h3>
          <ul>
            {(improvements || []).map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      <ResumeTips title="What to Change to Increase Your Score" />
    </div>
  );
}

export default ScoreCard;
