import React from 'react';
import StockList from './StockList';

function App() {
  const stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA'];

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