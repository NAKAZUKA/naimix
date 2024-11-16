import axios from 'axios';

const API_URL = 'http://localhost:8000/'; // URL вашего API

// Получить все элементы
export const fetchItems = async () => {
  const response = await axios.get(`${API_URL}/items`);
  return response.data;
};

// Создать новый элемент
export const createItem = async (item) => {
  const response = await axios.post(`${API_URL}/items`, item);
  return response.data;
};

// Обновить элемент
export const updateItem = async (id, item) => {
  const response = await axios.put(`${API_URL}/items/${id}`, item);
  return response.data;
};

// Удалить элемент
export const deleteItem = async (id) => {
  await axios.delete(`${API_URL}/items/${id}`);
};