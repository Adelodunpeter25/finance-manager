import { api } from './api';
import type { ReportData } from '../types/report';

export const reportService = {
  async getReportData(startDate?: string, endDate?: string): Promise<ReportData> {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await api.get<ReportData>(`/reports/?${params.toString()}`);
    return response.data;
  },

  async exportTransactions(startDate?: string, endDate?: string): Promise<Blob> {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const response = await api.get(`/reports/export/?${params.toString()}`, {
      responseType: 'blob'
    });
    return response.data;
  },
};
