import React from 'react';
import { Stock } from '../../../StockList';

interface CurrentTradingProps {
  stocks: Stock[];
}

const CurrentTrading: React.FC<CurrentTradingProps> = ({ stocks }) => {
  const tradingStocks = stocks.filter(stock => stock.isTrading);

  return (
    <div className="current-trading">
      <h2>Currently Trading</h2>
      <ul>
        {tradingStocks.map((stock, index) => (
          <li key={index}>
            <strong>{stock.name}</strong>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CurrentTrading;