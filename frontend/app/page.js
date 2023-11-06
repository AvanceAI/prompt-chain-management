"use client";
import UserInput from "@/components/UserInput"

export default function Home() {
  const websocket = new WebSocket('ws://localhost:8000/communicate');
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <UserInput websocket={websocket} />
    </main>
  )
}
