import React, { useState, useEffect, useRef } from 'react';
import ChainStarter from './ChainStarter';
import { MessageBox, Input, Button } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';

const UserInput = ({ websocket, mockMessage }) => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  
  const endOfMessagesRef = useRef(null);

  useEffect(() => {
    const handleMessageEvent = (data) => {
      setMessages((prevMessages) => [...prevMessages, { type: 'incoming', text: data.message.message, variable: data.message.variable, correlation_id: data.message.correlation_id }]);
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

  const renderMessage = (msg, index) => {
    if (msg.variable) {
      return (
        <div key={index}>
          <MessageBox
            position={msg.type === 'incoming' ? 'left' : 'right'}
            type={'text'}
            text={msg.text}
          />
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            {Object.keys(msg.variable).map((key) => (
              <Button
                key={key}
                text={key}
                onClick={() => handleButtonClick(key)}
              />
            ))}
          </div>
        </div>
      );
    } else {
      return (
        <MessageBox
          key={index}
          position={msg.type === 'incoming' ? 'left' : 'right'}
          type={'text'}
          text={msg.text}
        />
      );
    }
  };

  return (
    <div>
      <ChainStarter websocket={websocket} />
      {/* Display messages */}
      <div style={{ maxHeight: '500px', width: '800px', overflowY: 'auto', border: '1px solid black', margin: '10px' }}>
        {messages.map(renderMessage)}
      </div>

      {/* Input field */}
      <Input
        placeholder="Enter your input here"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendInput()}
        rightButtons={
          <Button
            color='white'
            backgroundColor='black'
            text='Send'
            onClick={sendInput}
          />
        }
      />
    </div>
  );
};

export default UserInput;