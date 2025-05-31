import React from "react";
import PDFToText from "react-pdftotext";
import mammoth from "mammoth";

function FileUpload({ onTextExtracted }) {
  // Triggered on file selection
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const fileType = file.name.split('.').pop().toLowerCase();

    if (fileType === "pdf") {
      try {
        const text = await parsePDF(file);
        onTextExtracted(text);
      } catch (err) {
        console.error("PDF parsing failed:", err);
        alert("Failed to parse PDF file.");
      }
    } else if (fileType === "docx") {
      try {
        const text = await parseDocx(file);
        onTextExtracted(text);
      } catch (err) {
        console.error("DOCX parsing failed:", err);
        alert("Failed to parse Word file.");
      }
    } else {
      alert("Unsupported file type. Please upload a PDF or DOCX.");
    }
  };

  // 🧾 PDF Parsing using react-pdftotext
  const parsePDF = async (file) => {
    const text = await PDFToText(file);
    console.log(text, "hi")
    return text;
  };

  // 📄 DOCX Parsing using mammoth
  const parseDocx = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value;
  };

  return (
    <div className="mb-4">
      <label className="block font-semibold mb-1">Upload Resume (PDF/DOCX)</label>
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
    </div>
  );
}

export default FileUpload;