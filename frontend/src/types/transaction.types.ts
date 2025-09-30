export type TransactionType = 'income' | 'expense';

export interface Transaction {
  id: number;
  category: number;
  category_name: string;
  amount: string;
  type: TransactionType;
  description: string;
  date: string;
  created_at: string;
  updated_at: string;
}

export interface TransactionFormData {
  category: number;
  amount: string;
  type: TransactionType;
  description: string;
  date: string;
}

export interface TransactionFilter {
  start_date?: string;
  end_date?: string;
  category?: number;
  type?: TransactionType;
  amount_min?: number;
  amount_max?: number;
}

export interface TransactionSummary {
  total_income: number;
  total_expenses: number;
  net_balance: number;
  monthly_breakdown: Array<{
    month: string;
    income: number | null;
    expenses: number | null;
  }>;
}
