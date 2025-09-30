export type BudgetPeriod = 'weekly' | 'monthly' | 'yearly';

export interface Budget {
  id: number;
  category: string;
  category_id: number;
  amount: number;
  period: BudgetPeriod;
  start_date: string;
  end_date: string;
  spent_amount: number;
  percentage: number;
  created_at: string;
}

export interface BudgetFormData {
  category_id: number;
  amount: number;
  period: BudgetPeriod;
  start_date: string;
  end_date: string;
}
