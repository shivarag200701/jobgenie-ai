import React, {useState} from "react";
import { dummyResponse } from "../dummyData";
import OutputViewer from "../components/outputViewer";
import FileUpload from "../components/fileUpload";

function ResumeUpload(){
    const [resumeText, setResumeText] = useState("");
    const [jobDesc, setJobDesc] = useState("");
    const [result, setResult] = useState(null);    

    const handleGenerate = () =>{
        setTimeout(() =>{
            setResult(dummyResponse);
        },1000)
    };

    return(
        <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">JobGenie</h1>


      <FileUpload onTextExtracted={(text) => setResumeText(text)} />

      <textarea
        className="w-full p-3 border rounded mb-4"
        rows={6}
        placeholder="Paste your resume here..."
        value={resumeText}
        onChange={(e) => setResumeText(e.target.value)}
      />

      <textarea
        className="w-full p-3 border rounded mb-4"
        rows={6}
        placeholder="Paste the job description here..."
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
      />

      <button
        onClick={handleGenerate}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Generate
      </button>

      {result && <OutputViewer data={result} />}
    </div>
    );
    };

export default ResumeUpload;


