"use client";

import { useState } from "react";

export default function Home() {
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async () => {
    if (!resume || !jobDescription) {
      alert("Please upload resume and paste job description");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);

      const response = await fetch("https://ats-backend-bk9n.onrender.com", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Error analyzing resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-lg">
        <h1 className="text-3xl font-extrabold mb-6 text-center bg-gradient-to-r from-indigo-600 to-pink-600 bg-clip-text text-transparent">

          ATS Resume Score Checker
        </h1>

        <label className="block mb-2 font-medium text-gray-800">Upload Resume</label>
       

<div className="flex items-center gap-3 mb-4">
  <label
    htmlFor="resume-upload"
     className="cursor-pointer bg-gradient-to-r from-indigo-600 to-pink-600
             text-white px-6 py-3 rounded-lg text-base font-medium
             hover:opacity-90 transition inline-flex items-center justify-center"
  >
    Choose Resume
  </label>

  <span className="text-sm text-gray-600">
    {resume ? resume.name : "No file chosen"}
  </span>
</div>

<input
  id="resume-upload"
  type="file"
  accept=".pdf,.docx"
  className="hidden"
  onChange={(e) => setResume(e.target.files?.[0] || null)}
/>


        <label className="block mb-2 font-medium text-gray-800">
          Paste Job Description
        </label>
        <textarea
          rows={6}
          className="w-full border rounded p-2 mb-4 text-gray-900"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button
          onClick={handleSubmit}
          
          className="w-full bg-gradient-to-r from-indigo-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:opacity-90 transition"

        >
          Analyze Resume
          
        </button>
        

{/* ===== ATS RESULT UI START ===== */}
{result && (
  <div className="mt-6 p-4 border rounded-lg">
    <h2 className="text-xl font-bold text-gray-900 mb-2">
      ATS Score: {result.final_ats_score}/100
    </h2>

    <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
      <div
        className="bg-green-600 h-3 rounded-full"
        style={{ width: `${result.final_ats_score}%` }}
      ></div>
    </div>

    <div className="mb-3">
      <h3 className="font-semibold text-gray-800">Missing Keywords</h3>
      <ul className="list-disc list-inside text-sm text-gray-700">
        {result.missing_keywords.length > 0 ? (
          result.missing_keywords.map((kw: string, i: number) => (
            <li key={i}>{kw}</li>
          ))
        ) : (
          <li>None 🎉</li>
        )}
      </ul>
    </div>

    <div>
      <h3 className="font-semibold text-gray-800">Missing Sections</h3>
      <ul className="list-disc list-inside text-sm text-gray-700">
        {result.missing_sections.length > 0 ? (
          result.missing_sections.map((sec: string, i: number) => (
            <li key={i}>{sec}</li>
          ))
        ) : (
          <li>All sections present 🎉</li>
        )}
      </ul>
    </div>
  </div>
)}
{/* ===== ATS RESULT UI END ===== */}

      </div>
    </main>
  );
}

