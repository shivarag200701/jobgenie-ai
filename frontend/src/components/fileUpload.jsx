import React from "react";

function FileUpload({ onTextExtracted }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();

    reader.onload = (event) => {
      const fakeExtractedText = `• Experience with Python and FastAPI
• Built AI tools using OpenAI API
• Skilled in system design and resume parsing`;
      onTextExtracted(fakeExtractedText); // simulate parsed text
    };

    reader.readAsArrayBuffer(file); // Just to simulate a read action
  };

  return (
    <div className="mb-4">
      <label className="block font-semibold mb-1">Upload Resume (PDF/DOCX)</label>
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
    </div>
  );
}

export default FileUpload;