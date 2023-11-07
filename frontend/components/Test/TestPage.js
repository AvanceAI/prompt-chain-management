// TestPage.js
"use client";
import React, { useState } from 'react';
import UserInput from "@/components/UserInput";
import SideBar from "@/components/Test/SideBar";

export default function TestPage({websocket}) {
  const [mockMessage, setMockMessage] = useState(null);

  const handleMockMessage = (message) => {
    setMockMessage(message);
  };

  return (
    <div style={{ display: 'flex' }}>
      <SideBar onSendMockMessage={handleMockMessage} />
      <div className='align-items-left' style={{ marginLeft: '150px' }}>
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <UserInput websocket={websocket} mockMessage={mockMessage} />
        </main>
      </div>
    </div>
  )
}
