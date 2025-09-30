export type NotificationType = 'budget_exceeded' | 'new_transaction' | 'budget_warning';

export interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}
