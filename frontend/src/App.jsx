import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Transactions from './pages/Transactions';
import TransactionDetails from './pages/TransactionDetails';
import PredictForm from './pages/PredictForm';
import { ShieldCheck, Activity, Database, FileText } from 'lucide-react';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        {/* Sidebar */}
        <aside className="w-64 bg-gray-900 text-white flex flex-col">
          <div className="p-4 flex items-center gap-2 border-b border-gray-800">
            <ShieldCheck className="text-blue-400" size={28} />
            <h1 className="text-xl font-bold">AI Risk Manager</h1>
          </div>
          <nav className="flex-1 p-4 space-y-2">
            <Link to="/" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
              <Activity size={20} /> Dashboard
            </Link>
            <Link to="/transactions" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
              <Database size={20} /> Transactions
            </Link>
            <Link to="/predict" className="flex items-center gap-2 p-2 hover:bg-gray-800 rounded">
              <FileText size={20} /> New Analysis
            </Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          <header className="bg-white p-4 shadow-sm">
            <h2 className="text-xl font-semibold text-gray-800">Intelligent Payment Fraud Detection</h2>
          </header>
          <div className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/transactions" element={<Transactions />} />
              <Route path="/transactions/:id" element={<TransactionDetails />} />
              <Route path="/predict" element={<PredictForm />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
