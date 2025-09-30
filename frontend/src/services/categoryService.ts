import { api } from './api';
import type { Category, CategoryType } from '../types/category';

interface CategoryFormData {
  name: string;
  type: CategoryType;
}

export const categoryService = {
  async getCategories(): Promise<Category[]> {
    const response = await api.get<Category[]>('/categories/');
    return response.data;
  },

  async createCategory(data: CategoryFormData): Promise<Category> {
    const response = await api.post<Category>('/categories/', data);
    return response.data;
  },

  async updateCategory(id: number, data: Partial<CategoryFormData>): Promise<Category> {
    const response = await api.patch<Category>(`/categories/${id}/`, data);
    return response.data;
  },

  async deleteCategory(id: number): Promise<void> {
    await api.delete(`/categories/${id}/`);
  },
};
