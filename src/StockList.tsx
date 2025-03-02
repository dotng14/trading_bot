import React from 'react';

interface StockListProps {
  stocks: string[];
}

const StockList: React.FC<StockListProps> = ({ stocks }) => {
  return (
    <div className="stock-list">
      <h2>Stock List</h2>
      <ul>
        {stocks.map((stock, index) => (
          <li key={index}>
            {stock}
            <button onClick={() => alert(`More details about ${stock}`)}>More Detail</button>
            <button onClick={() => alert(`Trading ${stock}`)}>Trade This</button>
            <button onClick={() => alert(`Stopped trading ${stock}`)}>Stop Trade This</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StockList;