import React, {useState} from "react";
import { dummyResponse } from "../dummyData";
import OutputViewer from "../components/outputViewer";
import FileUpload from "../components/fileUpload";
import axios from "axios"

function ResumeUpload(){
    const [resumeText, setResumeText] = useState("");
    const [jobDesc, setJobDesc] = useState("");
    const [result, setResult] = useState(null);   
    const [role, setRole] = useState(null);

    const handleGenerate = async () => {
      try{
        const response = await axios.post("http://localhost:8000/generate",{
          resume:resumeText,
          job_description: jobDesc
        });

        setResult(response.data);
      }
      catch (error){
        console.log("Error generating output:".error)

      }
    };

    const handleClassify = async () => {
      try{
        const response = await axios.post("http://localhost:8000/classify-role",{ 
          job_description: jobDesc
        });
        setRole(response.data);
      }
      catch (error){
        console.log("Error classifying role:", error);
      }
    };

     
    const handleExtractRequirements = async () => {
      try{
        const response = await axios.post("http://localhost:8000/classify-role",{ 
          job_description: jobDesc
        });
        setRole(response.data);
      }
      catch (error){
        console.log("Error classifying role:", error);
      }
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
        onClick={() =>{
          handleGenerate();
          handleClassify();
        }}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Generate
      </button>
      {role && <p>Role: {role}</p>}

      {result && <OutputViewer data={result} />}
    </div>
    );
    };

export default ResumeUpload;


