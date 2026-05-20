import React from 'react';
import Layout from '@/components/Common/Layout';
import ChatInterface from '@/components/Chat/ChatInterface';

export default function Chat() {
  return (
    <Layout>
      <div className="h-[calc(100vh-8rem)] flex flex-col">
        <div className="mb-6">
          <h1 className="text-4xl font-bold text-white mb-2">💬 AI Chat Assistant</h1>
          <p className="text-gray-400">
            Ask questions about your infrastructure and get AI-powered answers
          </p>
        </div>

        <div className="flex-1">
          <ChatInterface />
        </div>
      </div>
    </Layout>
  );
}
