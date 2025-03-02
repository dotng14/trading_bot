import StockList, { Stock } from './StockList';
import React from 'react';

function Home() {


  return (
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
}

export default Home;