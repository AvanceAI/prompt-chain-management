# Prompt-Chain-Management

This repo consists of two main parts: 1. a Python backend (src & tests), and 2. A ReactJS Frontend.

## Current Status
A Schema for defining prompt chains has been created. You can see an example in tests/data/chain_fixture.json.

By defining our prompt chain entirely outside of the code (in a JSON), we unlock the ability to rapidly create different prompt chains.

The backend has mostly been finished, but not all of the "Agents" for the first prompt chain have been created already. 

The websocket connection and front-end works, but it has not been fully integrated with the backend. We can send messages and select basic options, but the functionality needs to be expanded and tested more.

## Miro Board
The Miro Board below shows a schematic of the system.
https://miro.com/app/board/uXjVNRAbMBs=/

## TODO

Investigate replacing with LangChain, Wrapping LangChain, or using LangChain modules.

Build specific scrapers from linkedin, instagram, Twitter.
