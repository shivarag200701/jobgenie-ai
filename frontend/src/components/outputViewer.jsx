import ResumePDF from "./resumePDF";
import { PDFDownloadLink } from "@react-pdf/renderer";
function OutputViewer({ data }) {
    return(
        <div className="mt-6 space-y-4">
      <div>
        <h2 className="text-xl font-semibold mb-1">🎯 Tailored Resume</h2>
        <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap break-words">{data.tailoredResume}</pre>
      </div>
      <PDFDownloadLink document={<ResumePDF resumeText={data.tailoredResume} />}fileName="Tailored_Resume.pdf">
        {({ loading }) =>
          loading ? "Generating PDF..." : (
            <button className="bg-blue-600 text-white px-4 py-2 rounded mt-4">
              Download Tailored Resume as PDF
            </button>
          )
        }
      </PDFDownloadLink>
      <div>
        <h2 className="text-xl font-semibold mb-1">📝 Cover Letter</h2>
        <pre className="bg-gray-100 p-3 rounded  whitespace-pre-wrap break-words">{data.coverLetter}</pre>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-1">✅ Fit Summary</h2>
        <pre className="bg-gray-100 p-3 rounded  whitespace-pre-wrap break-words">{data.fitSummary}</pre>
      </div>
    </div>
    );

}

export default OutputViewer;