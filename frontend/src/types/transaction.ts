export type TransactionType = 'income' | 'expense';

export interface Transaction {
  id: number;
  amount: number;
  type: TransactionType;
  category: string;
  date: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface TransactionFormData {
  amount: number;
  type: TransactionType;
  category_id: number;
  date: string;
  description: string;
}

export interface TransactionFilter {
  type?: TransactionType;
  category?: string;
  date_from?: string;
  date_to?: string;
  search?: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
