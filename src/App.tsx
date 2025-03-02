import React from 'react';
import StockList from './StockList';

function App() {
  const stocks = [
    { name: 'AAPL', price: 150.25, change: 1.2 },
    { name: 'GOOGL', price: 2750.50, change: -0.5 },
    { name: 'AMZN', price: 3400.00, change: 0.8 },
    { name: 'MSFT', price: 299.99, change: -1.1 },
    { name: 'TSLA', price: 800.45, change: 2.3 },
  ];

  return (
    <div className="app-container">
      <h1 className="app-title">Robinhood Auto Trading Bot</h1>
      <div className="titles">
        <div className="titles">Profit/Loss</div>
        <div className="titles">
          <StockList stocks={stocks} />
        </div>
        <div className="titles">Current trading stock</div>
      </div>
    </div>
  );
}

export default App;