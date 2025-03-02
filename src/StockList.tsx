import React from 'react';

interface Stock {
  name: string;
  price: number;
  change: number;
}

interface StockListProps {
  stocks: Stock[];
}

const StockList: React.FC<StockListProps> = ({ stocks }) => {
  return (
    <div className="stock-list">
      <h2>Stock List</h2>
      <ul>
        {stocks.map((stock, index) => (
          <li key={index}>
            <div>
              <strong>{stock.name}</strong> - ${stock.price.toFixed(2)} ({stock.change.toFixed(2)}%)
            </div>
            <button onClick={() => alert(`More details about ${stock.name}`)}>More Detail</button>
            <button onClick={() => alert(`Trading ${stock.name}`)}>Trade This</button>
            <button onClick={() => alert(`Stopped trading ${stock.name}`)}>Stop Trade This</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StockList;