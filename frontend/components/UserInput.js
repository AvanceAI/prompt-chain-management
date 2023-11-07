import React, { useState, useEffect, useRef } from 'react';
import ChainStarter from './ChainStarter';
import { inputStyle, buttonStyle } from './UserInputStyle';

const UserInput = ({ websocket, mockMessage }) => {
  const [message, setMessage] = useState('');
  const [userInput, setUserInput] = useState('');

  useEffect(() => {
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setMessage(data.message);
      } else if (data.status) {
        console.log(data.status);
      }
    };
  }, [websocket]);

  useEffect(() => {
    if (mockMessage) {
      setMessage(mockMessage);
    }
  }, [mockMessage]);

  const sendInput = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({ "type": "user_entry", "user_entry": userInput, "correlation_id": message.correlation_id }));
      console.log('Input sent');
      setUserInput('');
    }
  };

  return (
    <div>
      <ChainStarter websocket={websocket} />
      <br />
      <br />
      <p>{message.message}</p>
      <p>{JSON.stringify(message.variable)}</p>
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
};


export default UserInput;
