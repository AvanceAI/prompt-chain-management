"use client";
import UserInput from "@/components/UserInput"

export default function Home() {
  const websocket = new WebSocket('ws://127.0.0.1:8080');
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <UserInput websocket={websocket} />
    </main>
  )
}
