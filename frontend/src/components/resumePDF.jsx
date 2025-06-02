// src/components/ResumePDF.jsx
import React from "react";
import { Document, Page, Text, StyleSheet } from "@react-pdf/renderer";

// Define basic styles for the PDF
const styles = StyleSheet.create({
  page: {
    padding: 30,
    fontSize: 12,
    fontFamily: "Helvetica",
  },
  section: {
    marginBottom: 10,
  },
});

// ResumePDF accepts text content from props
const ResumePDF = ({ resumeText }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.section}>{resumeText}</Text>
    </Page>
  </Document>
);

export default ResumePDF;