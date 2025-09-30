export interface Budget {
  id: number;
  category: number;
  category_name: string;
  amount: string;
  period: string;
  start_date: string;
  end_date: string;
  created_at: string;
}

export interface BudgetFormData {
  category: number;
  amount: string;
  period: string;
  start_date: string;
  end_date: string;
}

export interface BudgetStatus {
  budget_amount: number;
  spent_amount: number;
  remaining_amount: number;
  percentage_used: number;
  is_exceeded: boolean;
}
