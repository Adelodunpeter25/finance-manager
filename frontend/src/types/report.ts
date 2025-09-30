export interface ReportData {
  totalIncome: number;
  totalExpenses: number;
  netBalance: number;
  categoryBreakdown: CategoryBreakdown[];
  monthlyTrends: MonthlyTrend[];
  incomeVsExpenses: IncomeVsExpense[];
}

export interface CategoryBreakdown {
  category: string;
  amount: number;
  percentage: number;
  type: 'income' | 'expense';
}

export interface MonthlyTrend {
  month: string;
  income: number;
  expenses: number;
  net: number;
}

export interface IncomeVsExpense {
  month: string;
  income: number;
  expenses: number;
}
