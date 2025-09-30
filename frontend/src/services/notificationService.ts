import { api } from './api.config';
import type { Notification, PaginatedResponse } from '../types';

export const notificationService = {
  async getNotifications(): Promise<PaginatedResponse<Notification>> {
    const response = await api.get<PaginatedResponse<Notification>>('/notifications/');
    return response.data;
  },

  async markAsRead(id: number): Promise<void> {
    await api.patch(`/notifications/${id}/mark_read/`);
  },

  async markAllAsRead(): Promise<void> {
    await api.patch('/notifications/mark_all_read/');
  },
};
