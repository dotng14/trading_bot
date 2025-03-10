import React from 'react';
import StockList from './StockList';

const Home: React.FC = () => {

  return (
    <div className="app-container">
      <h1 className="app-title">Robinhood Auto Trading Bot</h1>
      <div className="titles">
        <div className="titles">Profit/Loss</div>
        <div className="titles">
          <StockList />
        </div>
      </div>
    </div>
  );
};

export default Home;