import React, { useState, useEffect } from 'react';

function UserInput({ websocket }) {
  const [message, setMessage] = useState('');
  const [userInput, setUserInput] = useState('');

  useEffect(() => {
    // Listen for messages on the websocket connection
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data && data.message) {
        setMessage(data.message);
      }
    };
  }, [websocket]);

  const sendInput = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({ userInput }));
      setUserInput(''); // Clear input field after sending
    }
  };

  const inputStyle = {
    width: '600px', // Making the input box wider
    height: '300px',
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
    <div>
      <p>{message}</p>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Enter your input here"
        style={inputStyle}
      />
      <button onClick={sendInput} style={buttonStyle}>
        Send
      </button>
    </div>
  );
}

export default UserInput;