"use client";
import TestPage from "@/components/Test/TestPage";

export default function Home() {
  const websocket = new WebSocket('ws://localhost:8000/communicate');
  return (
    <>
        <TestPage websocket={websocket} />
    </>
  )
}
