import React, { useState } from 'react';
import CurrentTrading from './CurrentTrading';

export interface Stock {
  name: string;
  price: number;
  day_change: number;
  isTrading?: boolean;
}

interface StockListProps {
  stocks: Stock[];
}

const StockList: React.FC<StockListProps> = ({ stocks }) => {
  const [stockList, setStockList] = useState(stocks);

  const toggleTrading = (index: number) => {
    const updatedStocks = stockList.map((stock, i) => 
      i === index ? { ...stock, isTrading: !stock.isTrading } : stock
    );
    setStockList(updatedStocks);
    console.log(updatedStocks); // Log the updated state
  };

  return (
    <div className="stock-list">
      <h2>Stock List</h2>
      <ul>
        {stockList.map((stock, index) => (
          <li key={index}>
            <div>
              <strong>{stock.name}</strong> 
              <p>Price: ${stock.price}</p>
            </div>
            <button onClick={() => alert(`More details about ${stock.name}`)}>More Detail</button>
            <button onClick={() => toggleTrading(index)}>
              {stock.isTrading ? 'Stop Trade This' : 'Trade This'}
            </button>
          </li>
        ))}
      </ul>
      <CurrentTrading stocks={stockList} />
    </div>
  );
};

export default StockList;