import React, { useEffect, useState, useRef } from 'react';
import { getTransactions, uploadCSV } from '../services/api';
import { Link } from 'react-router-dom';
import { Upload } from 'lucide-react';

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [filter, setFilter] = useState('');
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchData(filter);
  }, [filter]);

  const fetchData = (riskLevel) => {
    const params = riskLevel ? { risk_level: riskLevel } : {};
    getTransactions(params).then(res => {
      if (res.data.error) {
        setTransactions([]);
        alert(res.data.error);
      } else if (Array.isArray(res.data)) {
        setTransactions(res.data);
      } else {
        setTransactions([]);
      }
    }).catch(console.error);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await uploadCSV(formData);
      alert(res.data.message);
      fetchData(filter); // Refresh list
    } catch (err) {
      alert(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div className="bg-white p-6 rounded shadow">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">Transactions History</h2>
        <div className="flex gap-4">
          <input 
            type="file" 
            accept=".csv" 
            className="hidden" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
          />
          <button 
            onClick={() => fileInputRef.current?.click()} 
            disabled={uploading}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-blue-400"
          >
            <Upload size={18} /> {uploading ? 'Uploading...' : 'Upload CSV'}
          </button>
          
          <select 
            className="border rounded p-2"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="">All Risks</option>
            <option value="HIGH">High Risk</option>
            <option value="MEDIUM">Medium Risk</option>
            <option value="LOW">Low Risk</option>
          </select>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b text-sm text-gray-600">
              <th className="p-3">ID</th>
              <th className="p-3">Time</th>
              <th className="p-3">Amount</th>
              <th className="p-3">Risk Score</th>
              <th className="p-3">Level</th>
              <th className="p-3">Action</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(txn => (
              <tr key={txn.transaction_id} className="border-b hover:bg-gray-50">
                <td className="p-3 font-medium text-sm">{txn.transaction_id}</td>
                <td className="p-3 text-sm text-gray-600">{new Date(txn.transaction_time).toLocaleString()}</td>
                <td className="p-3 text-sm">₹{txn.transaction_amount}</td>
                <td className="p-3 text-sm">{txn.prediction.risk_score}</td>
                <td className="p-3 text-sm">
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    txn.prediction.risk_level === 'HIGH' ? 'bg-red-100 text-red-700' :
                    txn.prediction.risk_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-green-100 text-green-700'
                  }`}>
                    {txn.prediction.risk_level}
                  </span>
                </td>
                <td className="p-3">
                  <Link to={`/transactions/${txn.transaction_id}`} className="text-blue-600 hover:underline text-sm font-medium">
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
            {transactions.length === 0 && (
              <tr><td colSpan="6" className="p-4 text-center text-gray-500">No transactions found.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
