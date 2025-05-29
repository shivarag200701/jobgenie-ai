
function OutputViewer({ data }) {
    return(
        <div className="mt-6 space-y-4">
      <div>
        <h2 className="text-xl font-semibold mb-1">🎯 Tailored Resume</h2>
        <pre className="bg-gray-100 p-3 rounded">{data.tailoredResume}</pre>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-1">📝 Cover Letter</h2>
        <pre className="bg-gray-100 p-3 rounded">{data.coverLetter}</pre>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-1">✅ Fit Summary</h2>
        <pre className="bg-gray-100 p-3 rounded">{data.fitSummary}</pre>
      </div>
    </div>
    );

}

export default OutputViewer;