// Exchange rates relative to NGN (Nigerian Naira)
const EXCHANGE_RATES: Record<string, number> = {
  NGN: 1,
  USD: 0.0012,    // 1 NGN = 0.0012 USD
  EUR: 0.0011,    // 1 NGN = 0.0011 EUR
  GBP: 0.00095,   // 1 NGN = 0.00095 GBP
};

export const convertCurrency = (amount: number, fromCurrency: string, toCurrency: string): number => {
  if (fromCurrency === toCurrency) return amount;
  
  // Convert to NGN first, then to target currency
  const amountInNGN = amount / EXCHANGE_RATES[fromCurrency];
  return amountInNGN * EXCHANGE_RATES[toCurrency];
};

export const formatCurrency = (amount: number, currency: string): string => {
  const symbols: Record<string, string> = {
    NGN: '₦',
    USD: '$',
    EUR: '€',
    GBP: '£',
  };
  
  return `${symbols[currency] || currency} ${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
};
