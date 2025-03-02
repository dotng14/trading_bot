import StockList, { Stock } from './StockList';

function App() {
  const stocks: Stock[] = [
    { name: 'AAPL', isTrading: true},
    { name: 'GOOGL', isTrading: false},
    { name: 'AMZN' , isTrading: false},
    { name: 'MSFT', isTrading: false},
    { name: 'TSLA', isTrading: false},
  ];

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

export default App;