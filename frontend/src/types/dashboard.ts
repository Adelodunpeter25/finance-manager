export interface DashboardStats {
  totalIncome: number;
  totalExpenses: number;
  netBalance: number;
  budgetUtilization: number;
}

export interface RecentTransaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category: string;
  date: string;
  description: string;
}

export interface BudgetStatus {
  id: number;
  category: string;
  budgetAmount: number;
  spentAmount: number;
  percentage: number;
}
