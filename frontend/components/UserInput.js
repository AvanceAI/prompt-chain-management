import React, { useState, useEffect, useRef } from 'react';
import ChainStarter from './ChainStarter';
import { inputStyle, buttonStyle } from './UserInputStyle';

const UserInput = ({ websocket, mockMessage }) => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  
  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    const handleMessageEvent = (data) => {
      setMessages((prevMessages) => [...prevMessages, { type: 'incoming', text: data.message.message, variable: data.message.variable }]);
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        handleMessageEvent(data);
      } else if (data.status) {
        console.log(data.status);
      }
    };
  }, [websocket]);

  useEffect(() => {
    if (mockMessage) {
      setMessages((prevMessages) => [...prevMessages, { type: 'incoming', text: mockMessage.message, variable: mockMessage.variable }]);
    }
  }, [mockMessage]);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendInput = () => {
    if (websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({ "type": "user_entry", "user_entry": userInput, "correlation_id": messages[messages.length - 1]?.correlation_id }));
      setMessages((prevMessages) => [...prevMessages, { type: 'outgoing', text: userInput }]);
      console.log('Input sent');
      setUserInput('');
    }
  };

  const handleButtonClick = (key) => {
    console.log(key);
  };

  return (
    <div>
      <ChainStarter websocket={websocket} />
      <div style={{ maxHeight: '500px', width: '800px', overflowY: 'auto', border: '1px solid black', margin: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index}>
            <p style={msg.type === 'incoming' ? { color: 'blue' } : { color: 'green' }}>{msg.text}</p>
            {msg.variable && (
              <div style={{ display: 'flex', flexDirection: 'row' }}> {/* This line is new */}
                {Object.keys(msg.variable).map((key) => (
                  <button key={key} onClick={() => handleButtonClick(key)} style={{ ...buttonStyle, margin: '0 4px' }}> {/* Adjusted style */}
                    {key}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        <div ref={endOfMessagesRef} />
      </div>

      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Enter your input here"
        style={inputStyle}
        onKeyPress={(e) => e.key === 'Enter' && sendInput()}
      />
      <button onClick={sendInput} style={buttonStyle}>
        Send
      </button>
    </div>
  );
};

export default UserInput;
