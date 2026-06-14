import { ATS_TIPS } from "../config/site";
import "./ResumeTips.css";

function ResumeTips({ title = "How to Improve Your ATS Score" }) {
  return (
    <section className="resume-tips">
      <h3>{title}</h3>
      <p className="resume-tips-intro">
        A higher ATS score means your resume is easier for hiring systems to read and rank.
        Focus on the changes below to strengthen your next version.
      </p>
      <ul>
        {ATS_TIPS.map((tip, index) => (
          <li key={index}>{tip}</li>
        ))}
      </ul>
    </section>
  );
}

export default ResumeTips;
