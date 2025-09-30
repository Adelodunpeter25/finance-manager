import { api } from './api';
import type { Budget, BudgetFormData } from '../types/budget';

export const budgetService = {
  async getBudgets(): Promise<Budget[]> {
    const response = await api.get<Budget[]>('/budgets/');
    return response.data;
  },

  async getBudget(id: number): Promise<Budget> {
    const response = await api.get<Budget>(`/budgets/${id}/`);
    return response.data;
  },

  async createBudget(data: BudgetFormData): Promise<Budget> {
    const response = await api.post<Budget>('/budgets/', data);
    return response.data;
  },

  async updateBudget(id: number, data: Partial<BudgetFormData>): Promise<Budget> {
    const response = await api.patch<Budget>(`/budgets/${id}/`, data);
    return response.data;
  },

  async deleteBudget(id: number): Promise<void> {
    await api.delete(`/budgets/${id}/`);
  },
};
