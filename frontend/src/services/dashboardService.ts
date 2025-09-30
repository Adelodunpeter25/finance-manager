import { api } from './api';
import type { DashboardStats, RecentTransaction, BudgetStatus } from '../types/dashboard';

export const dashboardService = {
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await api.get<DashboardStats>('/dashboard/stats/');
    return response.data;
  },

  async getRecentTransactions(): Promise<RecentTransaction[]> {
    const response = await api.get<RecentTransaction[]>('/dashboard/recent-transactions/');
    return response.data;
  },

  async getBudgetStatus(): Promise<BudgetStatus[]> {
    const response = await api.get<BudgetStatus[]>('/dashboard/budget-status/');
    return response.data;
  },
};
