import React, { useState, useEffect } from 'react';
import StockList, { Stock } from './StockList';

async function GetStockData(name: string) {
  const response = await fetch('http://127.0.0.1:5000/basic_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name }),
  });
  const data = await response.json();
  return {
    name: name,
    price: data.price === null ? 0 : data.price,
    day_change: data.day_change === null ? 0 : data.day_change,
  };
}

async function GetStockList() {
  const response = await fetch('http://127.0.0.1:5000/stock_list', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  const names : string[] = data.stock_list;

  const stockPromises = names.map(name => GetStockData(name));
  const stocks : Stock[] = await Promise.all(stockPromises);
  return stocks;
}

const Home: React.FC = () => {
  const [stocks, setStocks] = useState<Stock[]>([]);

  useEffect(() => {
    async function fetchStocks() {
      const stockList = await GetStockList();
      setStocks(stockList);
    }

    fetchStocks(); // Initial fetch

    const intervalId = setInterval(fetchStocks, 5000); // Fetch every 30 seconds

    return () => clearInterval(intervalId); // Cleanup interval on component unmount
  }, []);

  useEffect(() => {
    console.log(stocks);
  }, [stocks]);

  if (stocks.length > 0) return (
    <div className="app-container">
      <h1 className="app-title">Robinhood Auto Trading Bot</h1>
      <div className="titles">
        <div className="titles">Profit/Loss</div>
        <div className="titles">
          <StockList stocks={stocks} />
        </div>
      </div>
    </div>
  );
  else return (
    <div className="app-container">
      <h1 className="app-title">Robinhood Auto Trading Bot</h1>
      <p>Loading...</p>
    </div>
  );
};

export default Home;