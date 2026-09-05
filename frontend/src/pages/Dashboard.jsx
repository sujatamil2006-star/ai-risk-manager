import React, { useEffect, useState } from 'react';
import { getDashboardStats, getModelMetrics } from '../services/api';
import { ShieldAlert, CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    getDashboardStats().then(res => setStats(res.data)).catch(console.error);
    getModelMetrics().then(res => setMetrics(res.data)).catch(console.error);
  }, []);

  if (!stats) return <div className="p-4">Loading dashboard...</div>;

  const s = stats.stats;
  
  return (
    <div className="space-y-6">
      {/* Stats row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded shadow border-l-4 border-blue-500">
          <div className="text-gray-500 text-sm">Total Transactions</div>
          <div className="text-2xl font-bold">{s.total_transactions}</div>
        </div>
        <div className="bg-white p-4 rounded shadow border-l-4 border-red-500">
          <div className="text-gray-500 text-sm flex items-center gap-1"><ShieldAlert size={16}/> High Risk</div>
          <div className="text-2xl font-bold text-red-600">{s.high_risk}</div>
        </div>
        <div className="bg-white p-4 rounded shadow border-l-4 border-yellow-500">
          <div className="text-gray-500 text-sm flex items-center gap-1"><AlertTriangle size={16}/> Medium Risk</div>
          <div className="text-2xl font-bold text-yellow-600">{s.medium_risk}</div>
        </div>
        <div className="bg-white p-4 rounded shadow border-l-4 border-green-500">
          <div className="text-gray-500 text-sm flex items-center gap-1"><CheckCircle size={16}/> Average Risk Score</div>
          <div className="text-2xl font-bold">{s.average_risk_score}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {/* Recent High Risk */}
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold text-lg border-b pb-2 mb-4">Recent High Risk Transactions</h3>
          {stats.recent_high_risk && stats.recent_high_risk.length > 0 ? (
            <div className="space-y-3">
              {stats.recent_high_risk.map(txn => (
                <div key={txn.transaction_id} className="flex justify-between items-center p-3 bg-red-50 rounded border border-red-100">
                  <div>
                    <div className="font-medium">{txn.transaction_id}</div>
                    <div className="text-sm text-gray-600">₹{txn.transaction_amount} - {txn.merchant_category}</div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-xs text-red-500 font-bold">Risk: {txn.prediction.risk_score}</div>
                    </div>
                    <Link to={`/transactions/${txn.transaction_id}`} className="px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700">
                      Review
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-gray-500 py-4 text-center">No high risk transactions found.</div>
          )}
        </div>
      </div>
    </div>
  );
}
