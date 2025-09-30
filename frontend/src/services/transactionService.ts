import { api } from './api';
import type { Transaction, TransactionFormData, TransactionFilter, PaginatedResponse } from '../types/transaction';

export const transactionService = {
  async getTransactions(params?: TransactionFilter): Promise<PaginatedResponse<Transaction>> {
    const response = await api.get<PaginatedResponse<Transaction>>('/transactions/', { params });
    return response.data;
  },

  async getTransaction(id: number): Promise<Transaction> {
    const response = await api.get<Transaction>(`/transactions/${id}/`);
    return response.data;
  },

  async createTransaction(data: TransactionFormData): Promise<Transaction> {
    const response = await api.post<Transaction>('/transactions/', data);
    return response.data;
  },

  async updateTransaction(id: number, data: Partial<TransactionFormData>): Promise<Transaction> {
    const response = await api.patch<Transaction>(`/transactions/${id}/`, data);
    return response.data;
  },

  async deleteTransaction(id: number): Promise<void> {
    await api.delete(`/transactions/${id}/`);
  },
};
