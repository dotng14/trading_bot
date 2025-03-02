import StockList from './StockList';

function Home() {
  const stocks = [
    {name: 'AAPL', price: 100, quantity: 10},
    {name: 'GOOGL', price: 2000, quantity: 5},
    {name: 'TSLA', price: 500, quantity: 2}
  ]

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