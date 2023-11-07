import React, { useState } from 'react';
import { inputStyle, buttonStyle } from './ChainStarterStyle';

function ChainStarter({ websocket }) {
  const [filePath, setFilePath] = useState('');

  const startChainExecution = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      // Add a "type" field to the message
      websocket.send(JSON.stringify({ type: 'startChain', filePath }));
    }
  };
  
  return (
    <div className='text-center'>
      <input
        type="text"
        value={filePath}
        onChange={(e) => setFilePath(e.target.value)}
        placeholder="Enter the file path for chain data"
        style={inputStyle}
      />
      <button onClick={startChainExecution} style={buttonStyle}>Start</button>
    </div>
  );
}

export default ChainStarter;
