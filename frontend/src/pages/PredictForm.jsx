import React, { useState } from 'react';
import { predictTransaction } from '../services/api';

export default function PredictForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({
    transaction_id: `MANUAL_${Math.floor(Math.random() * 10000)}`,
    user_id: 'USER0001',
    transaction_amount: 1500,
    transaction_time: new Date().toISOString().slice(0, 19).replace('T', ' '),
    location: 'Mumbai',
    device: 'Android',
    merchant_category: 'Retail',
    payment_method: 'Credit Card'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'transaction_amount' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const res = await predictTransaction(formData);
      setResult(res.data);
    } catch (e) {
      alert('Prediction failed. ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="bg-white p-8 rounded shadow">
        <h2 className="text-2xl font-bold mb-6">Analyze Single Transaction</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Transaction ID</label>
              <input name="transaction_id" value={formData.transaction_id} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">User ID</label>
              <input name="user_id" value={formData.user_id} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Amount (₹)</label>
              <input type="number" name="transaction_amount" value={formData.transaction_amount} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Time (YYYY-MM-DD HH:MM:SS)</label>
              <input name="transaction_time" value={formData.transaction_time} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
              <input name="location" value={formData.location} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Device</label>
              <input name="device" value={formData.device} onChange={handleChange} className="w-full border p-2 rounded" required />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Merchant Category</label>
              <select name="merchant_category" value={formData.merchant_category} onChange={handleChange} className="w-full border p-2 rounded">
                <option>Retail</option>
                <option>Travel</option>
                <option>Food</option>
                <option>Entertainment</option>
                <option>Electronics</option>
                <option>Utilities</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
              <select name="payment_method" value={formData.payment_method} onChange={handleChange} className="w-full border p-2 rounded">
                <option>Credit Card</option>
                <option>Debit Card</option>
                <option>UPI</option>
                <option>Net Banking</option>
              </select>
            </div>
          </div>

          <div className="pt-4 border-t mt-6">
            <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white p-3 rounded font-bold hover:bg-blue-700 disabled:bg-blue-400">
              {loading ? 'Analyzing...' : 'Analyze Transaction'}
            </button>
          </div>

        </form>
      </div>

      {result && (
        <div className="bg-white p-6 rounded shadow border-t-4 border-blue-500">
          <h3 className="text-lg font-semibold border-b pb-2 mb-4">AI Risk Assessment Result</h3>
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="bg-gray-50 p-3 rounded flex-1">
                <div className="text-xs text-gray-500">Risk Score</div>
                <div className="text-xl font-bold">{result.risk_score}/100</div>
              </div>
              <div className="bg-gray-50 p-3 rounded flex-1">
                <div className="text-xs text-gray-500">Fraud Prob.</div>
                <div className="text-xl font-bold">{(result.fraud_probability * 100).toFixed(1)}%</div>
              </div>
              <div className="bg-gray-50 p-3 rounded flex-1">
                <div className="text-xs text-gray-500">Anomaly</div>
                <div className="text-xl font-bold">{result.anomaly_status}</div>
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded text-sm text-blue-900 border border-blue-100">
              <strong>AI Explanation:</strong>
              <p className="mt-1">{result.ai_explanation}</p>
            </div>
            
            <div>
              <h4 className="font-medium text-sm text-gray-700 mb-2">Top Risk Factors</h4>
              <ul className="list-disc pl-5 text-sm text-red-600 space-y-1">
                {result.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
                {result.risk_factors.length === 0 && <li className="text-gray-500">None</li>}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
