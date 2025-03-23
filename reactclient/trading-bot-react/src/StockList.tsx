import React from 'react';
import CurrentTrading from './CurrentTrading';
import Modal, { StockData } from './Modal';

async function GetStockList() {
  const response = await fetch('http://127.0.0.1:5000/stock_list', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const data = await response.json();
  const stocks: Stock[] = data.stock_list.map((stock: Stock) =>
  {return { ...stock, isTrading: false };}
  );
  return stocks;
}

async function GetAdvancedData(ticker: string): Promise<StockData> {
  const response = await fetch('http://127.0.0.1:5000/advanced_data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ticker }),
  });
  const data = await response.json();
  return data.data;
}

async function saveStock(stocks: Stock[]) {
  await fetch('http://127.0.0.1:5000/save_stock', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({  stocks }),
  });
}

export interface Stock {
  ticker: string;
  price: number;
  day_change: number;
  isTrading?: boolean;
}

class StockList extends React.Component<any, any, Stock[]> {
  state = {
    stocks: [] as Stock[],
    isModalOpen: false,
    advancedData: null as StockData | null,
  };

  async fetchStocks() {
    const newStocks = await GetStockList();
    const updatedStocks = newStocks.map(newStock => {
      const existingStock = this.state.stocks.find(stock => stock.ticker === newStock.ticker);
      return existingStock
        ? { ...newStock, isTrading: existingStock.isTrading }
        : newStock;
    });
    this.setState({ stocks: updatedStocks });
  }

  async fetchAdvancedData(ticker: string) {
    const advancedData = await GetAdvancedData(ticker);
    this.setState({ advancedData : advancedData, isModalOpen: true });
  }

  toggleTrading(index: number) {
    const updatedStocks = this.state.stocks.map((stock: Stock, i: number) =>
      i === index ? { ...stock, isTrading: !stock.isTrading } : stock
    );
    this.setState({ stocks: updatedStocks });
    saveStock(updatedStocks);
    console.log(updatedStocks); // Log the updated state
  }

  constructor(props: any) {
    super(props);
    this.state = {
      stocks: [] as Stock[],
      isModalOpen: false,
      advancedData: null,
    };
    this.fetchStocks(); // Initial fetch
    setInterval(() => this.fetchStocks(), 5000); // Fetch every 5 seconds
  }

  render() {
    if (this.state.stocks.length === 0) return <div>Loading...</div>;
    else
      return (
        <div className="stock-list">
          <h2>Stock List</h2>
          <ul>
            {this.state.stocks.map((stock: Stock, index: number) => (
              <li key={index}>
                <div>
                  <strong>{stock.ticker}</strong>
                  <p>Price: ${stock.price} ({stock.day_change}%)</p>
                </div>
                <button onClick={() => this.fetchAdvancedData(stock.ticker)}>More Detail</button>
                <button onClick={() => this.toggleTrading(index)}>
                  {stock.isTrading ? 'Stop Trade This' : 'Trade This'}
                </button>
              </li>
            ))}
            <Modal
            isOpen={this.state.isModalOpen}
            onClose={() => this.setState({ isModalOpen: false })}
            data={this.state.advancedData}
          />
          </ul>
          <CurrentTrading stocks={this.state.stocks} />
        </div>
      );
  }
}

export default StockList;