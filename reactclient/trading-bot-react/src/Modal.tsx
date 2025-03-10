import React from 'react';
import './Modal.css'; // Add some basic styling for the modal

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: StockData | null;
}

export interface StockData {
  description: string;
  name: string;
  price: number;
  day_change: number;
  open: number;
  high: number;
  low: number;
  volume: number;
  average_volume: number;
  market_cap: number;
  pe_ratio: number;
  dividend_yield: number;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, data }) => {
  if (!isOpen || !data) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <h2>{data.name}</h2>
        <p>{data.description}</p>
        <ul>
          <li>Price: ${data.price}</li>
          <li>Day Change: {data.day_change}%</li>
          <li>Open: ${data.open}</li>
          <li>High: ${data.high}</li>
          <li>Low: ${data.low}</li>
          <li>Volume: {data.volume}</li>
          <li>Average Volume: {data.average_volume}</li>
          <li>Market Cap: {data.market_cap}</li>
          <li>PE Ratio: {data.pe_ratio}</li>
          <li>Dividend Yield: {data.dividend_yield}%</li>
        </ul>
      </div>
    </div>
  );
};

export default Modal;