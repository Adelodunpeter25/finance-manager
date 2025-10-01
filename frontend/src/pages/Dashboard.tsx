import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { dashboardService } from '../services/dashboardService';
import type { DashboardStats, RecentTransaction, BudgetStatus } from '../types/dashboard';

const Dashboard: React.FC = React.memo(() => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [recentTransactions, setRecentTransactions] = useState<RecentTransaction[]>([]);
  const [budgetStatus, setBudgetStatus] = useState<BudgetStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [statsData, transactionsData, budgetsData] = await Promise.all([
          dashboardService.getDashboardStats(),
          dashboardService.getRecentTransactions(),
          dashboardService.getBudgetStatus()
        ]);

        setStats(statsData);
        setRecentTransactions(transactionsData);
        setBudgetStatus(budgetsData);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-lg text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-6 text-gray-900">
          Welcome back, {user?.first_name || user?.username}!
        </h1>
        
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Total Income</h3>
            <p className="text-3xl font-bold text-green-600">
              ${stats?.totalIncome.toFixed(2)}
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Total Expenses</h3>
            <p className="text-3xl font-bold text-red-600">
              ${stats?.totalExpenses.toFixed(2)}
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Net Balance</h3>
            <p className={`text-3xl font-bold ${stats && stats.netBalance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              ${stats?.netBalance.toFixed(2)}
            </p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Budget Usage</h3>
            <p className="text-3xl font-bold text-blue-600">
              {stats?.budgetUtilization}%
            </p>
          </div>
        </div>
        
        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Transactions */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-900">Recent Transactions</h2>
            {recentTransactions.length > 0 ? (
              <div className="space-y-3">
                {recentTransactions.map((transaction) => (
                  <div key={transaction.id} className="flex justify-between items-center py-2 border-b border-gray-100 last:border-b-0">
                    <div>
                      <p className="font-medium text-gray-900">{transaction.description}</p>
                      <p className="text-sm text-gray-500">{transaction.category} • {transaction.date}</p>
                    </div>
                    <span className={`font-semibold ${transaction.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                      {transaction.type === 'income' ? '+' : '-'}${transaction.amount.toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No recent transactions</p>
            )}
          </div>
          
          {/* Budget Overview */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-900">Budget Overview</h2>
            {budgetStatus.length > 0 ? (
              <div className="space-y-4">
                {budgetStatus.map((budget) => (
                  <div key={budget.id}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium text-gray-900">{budget.category}</span>
                      <span className="text-sm text-gray-600">
                        ${budget.spentAmount.toFixed(2)} / ${budget.budgetAmount.toFixed(2)}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${budget.percentage > 80 ? 'bg-red-500' : budget.percentage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}
                        style={{ width: `${Math.min(budget.percentage, 100)}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">{budget.percentage}% used</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No budgets set up yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
});

Dashboard.displayName = 'Dashboard';
export default Dashboard;
