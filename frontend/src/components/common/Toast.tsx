import React, { useEffect } from 'react';

interface ToastProps {
  message: string;
  type: 'success' | 'error';
  isVisible: boolean;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type, isVisible, onClose }) => {
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        onClose();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose]);

  if (!isVisible) return null;

  return (
    <div className="fixed top-4 right-4 z-50 animate-slide-in">
      <div className={`px-6 py-4 rounded-md shadow-lg max-w-md ${
        type === 'success' ? 'bg-white text-gray-800 border border-gray-200' : 'bg-red-500 text-white'
      }`}>
        <div className="font-medium text-base">
          {type === 'success' ? 'Welcome back!' : 'Error'}
        </div>
        <div className="text-base mt-2">
          {message}
        </div>
      </div>
    </div>
  );
};

export default Toast;
