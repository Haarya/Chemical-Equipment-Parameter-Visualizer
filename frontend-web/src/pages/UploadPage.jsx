/**
 * Upload Page - Chemistry Lab Edition
 * 
 * Dedicated page for CSV file upload with professional layout
 */

import React from 'react';
import Layout from '../components/Layout';
import FileUpload from '../components/FileUpload';

const UploadPage = () => {
  const handleUploadSuccess = () => {
    // Upload success is handled by FileUpload component's navigation
  };

  return (
    <Layout>
      <div className="container">
        <FileUpload onUploadSuccess={handleUploadSuccess} />
      </div>
    </Layout>
  );
};

export default UploadPage;
