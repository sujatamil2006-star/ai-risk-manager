import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getTransaction, submitReview } from '../services/api';

export default function TransactionDetails() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [comment, setComment] = useState('');

  useEffect(() => {
    getTransaction(id).then(res => setData(res.data)).catch(console.error);
  }, [id]);

  const handleReview = async (decision) => {
    try {
      await submitReview({
        transaction_id: id,
        decision,
        comment,
        analyst_id: 'ANALYST_01'
      });
      alert('Review submitted!');
      // Reload
      const res = await getTransaction(id);
      setData(res.data);
    } catch (e) {
      alert('Failed to submit review');
    }
  };

  if (!data) return <div className="p-6">Loading transaction...</div>;

  const { prediction, review } = data;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Transaction {id}</h2>
        {review && (
          <span className={`px-3 py-1 rounded font-bold text-sm ${review.decision === 'APPROVE' ? 'bg-green-100 text-green-800' : review.decision === 'REJECT' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
            Status: {review.decision}
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Details Card */}
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-lg font-semibold border-b pb-2 mb-4">Transaction Details</h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between"><span className="text-gray-500">Amount:</span> <span className="font-medium">₹{data.transaction_amount}</span></div>
            <div className="flex justify-between"><span className="text-gray-500">Time:</span> <span className="font-medium">{data.transaction_time}</span></div>
            <div className="flex justify-between"><span className="text-gray-500">User:</span> <span className="font-medium">{data.user_id}</span></div>
            <div className="flex justify-between"><span className="text-gray-500">Location:</span> <span className="font-medium">{data.location}</span></div>
            <div className="flex justify-between"><span className="text-gray-500">Device:</span> <span className="font-medium">{data.device}</span></div>
            <div className="flex justify-between"><span className="text-gray-500">Merchant:</span> <span className="font-medium">{data.merchant_category}</span></div>
          </div>
        </div>

        {/* AI Assessment Card */}
        {prediction ? (
          <div className="bg-white p-6 rounded shadow border-t-4 border-blue-500">
            <h3 className="text-lg font-semibold border-b pb-2 mb-4">AI Risk Assessment</h3>
            <div className="space-y-4">
              <div className="flex gap-4">
                <div className="bg-gray-50 p-3 rounded flex-1">
                  <div className="text-xs text-gray-500">Risk Score</div>
                  <div className="text-xl font-bold">{prediction.risk_score}/100</div>
                </div>
                <div className="bg-gray-50 p-3 rounded flex-1">
                  <div className="text-xs text-gray-500">Fraud Prob.</div>
                  <div className="text-xl font-bold">{(prediction.fraud_probability * 100).toFixed(1)}%</div>
                </div>
                <div className="bg-gray-50 p-3 rounded flex-1">
                  <div className="text-xs text-gray-500">Anomaly</div>
                  <div className="text-xl font-bold">{prediction.anomaly_status}</div>
                </div>
              </div>

              <div className="bg-blue-50 p-4 rounded text-sm text-blue-900 border border-blue-100">
                <strong>AI Explanation:</strong>
                <p className="mt-1">{prediction.ai_explanation}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-sm text-gray-700 mb-2">Top Risk Factors (SHAP)</h4>
                <ul className="list-disc pl-5 text-sm text-red-600 space-y-1">
                  {prediction.risk_factors.map((f, i) => <li key={i}>{f}</li>)}
                  {prediction.risk_factors.length === 0 && <li className="text-gray-500">None</li>}
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white p-6 rounded shadow border-t-4 border-gray-500">
            <h3 className="text-lg font-semibold border-b pb-2 mb-4">AI Risk Assessment</h3>
            <p className="text-gray-500">Prediction data not found or database is unavailable.</p>
          </div>
        )}
      </div>

      {/* Review Action */}
      {!review && prediction && (
        <div className="bg-white p-6 rounded shadow border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Analyst Action</h3>
          <textarea 
            className="w-full border rounded p-3 mb-4 text-sm" 
            rows="3" 
            placeholder="Analyst comments..."
            value={comment}
            onChange={e => setComment(e.target.value)}
          ></textarea>
          <div className="flex gap-4">
            <button onClick={() => handleReview('APPROVE')} className="px-6 py-2 bg-green-600 text-white rounded font-medium hover:bg-green-700">Approve</button>
            <button onClick={() => handleReview('INVESTIGATE')} className="px-6 py-2 bg-yellow-500 text-white rounded font-medium hover:bg-yellow-600">Investigate</button>
            <button onClick={() => handleReview('REJECT')} className="px-6 py-2 bg-red-600 text-white rounded font-medium hover:bg-red-700">Reject</button>
          </div>
        </div>
      )}
    </div>
  );
}
