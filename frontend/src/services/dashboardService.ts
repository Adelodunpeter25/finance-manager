import { api } from './api';
import { apiCache } from '../utils/cache';
import type { DashboardStats, RecentTransaction, BudgetStatus } from '../types/dashboard';

export const dashboardService = {
  async getDashboardStats(): Promise<DashboardStats> {
    const cacheKey = 'dashboard-stats';
    const cached = apiCache.get<DashboardStats>(cacheKey);
    if (cached) return cached;

    const response = await api.get<DashboardStats>('/dashboard/stats/');
    apiCache.set(cacheKey, response.data, 300000);
    return response.data;
  },

  async getRecentTransactions(): Promise<RecentTransaction[]> {
    const cacheKey = 'recent-transactions';
    const cached = apiCache.get<RecentTransaction[]>(cacheKey);
    if (cached) return cached;

    const response = await api.get<RecentTransaction[]>('/dashboard/recent-transactions/');
    apiCache.set(cacheKey, response.data, 60000);
    return response.data;
  },

  async getBudgetStatus(): Promise<BudgetStatus[]> {
    const cacheKey = 'budget-status';
    const cached = apiCache.get<BudgetStatus[]>(cacheKey);
    if (cached) return cached;

    const response = await api.get<BudgetStatus[]>('/dashboard/budget-status/');
    apiCache.set(cacheKey, response.data, 300000);
    return response.data;
  },
};
