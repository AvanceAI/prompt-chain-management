import React, { useState } from 'react';

function ChainStarter({ websocket }) {
  const [filePath, setFilePath] = useState('');

  const startChainExecution = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      // Add a "type" field to the message
      websocket.send(JSON.stringify({ type: 'startChain', filePath }));
    }
  };
  

  const inputStyle = {
    width: '400px', // Making the input box wider
    height: '50px',
    fontSize: '1.5em',
    border: '1px solid black',
    margin: '20px 0' // Add some vertical space
  };

  const buttonStyle = {
    width: '50%', // Making the button wider
    padding: '15px 0', // Making the button taller
    fontSize: '1.5em',
    margin: '0 auto', // Center button horizontally
    display: 'block', // Display button below the text box
    background: 'red'
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
