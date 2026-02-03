'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import Navbar from '@/components/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { FileText, Building2, ArrowRight, Users, Settings } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();

  return (
    <ProtectedRoute>
      <div className="min-h-screen relative overflow-hidden">
        {/* Background Image */}
        <div 
          className="fixed inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url(https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop)',
          }}
        >
          <div className="absolute inset-0 bg-gradient-to-br from-blue-900/80 via-purple-900/70 to-pink-900/80"></div>
        </div>
        
        {/* Grid pattern overlay */}
        <div className="fixed inset-0 opacity-10" style={{
          backgroundImage: `repeating-linear-gradient(0deg, transparent, transparent 2px, white 2px, white 3px),
                           repeating-linear-gradient(90deg, transparent, transparent 2px, white 2px, white 3px)`,
          backgroundSize: '50px 50px'
        }}></div>
        
        <div className="relative z-10">
          <Navbar activeTab="chat" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="inline-block mb-6">
              <div className="p-6 bg-white/10 backdrop-blur-md rounded-3xl shadow-2xl transform hover:scale-105 transition-transform border border-white/30">
                <svg className="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
            </div>
            <h1 className="text-6xl font-bold text-white mb-4 drop-shadow-2xl">
              Welcome to RAG Chat
            </h1>
            <p className="text-xl text-gray-100 max-w-3xl mx-auto leading-relaxed drop-shadow-lg">
              Intelligent document conversations powered by AI. Choose how you want to interact with your knowledge base.
            </p>
          </div>

          {/* Chat Options */}
          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {/* Chat with Document */}
            <Card className="hover:shadow-2xl transition-all duration-300 cursor-pointer group border border-white/30 bg-white/10 backdrop-blur-md hover:bg-white/20">
              <CardHeader>
                <div className="flex items-center justify-center mb-4">
                  <div className="p-6 bg-white/20 backdrop-blur-sm rounded-2xl group-hover:scale-110 transition-transform shadow-lg border border-white/40">
                    <FileText className="w-12 h-12 text-white" />
                  </div>
                </div>
                <CardTitle className="text-center text-3xl font-bold text-white drop-shadow-lg">
                  Chat with Document
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-100 mb-8 text-lg leading-relaxed">
                  Ask questions about a specific document and get instant, accurate answers based on its content.
                </p>
                <Button 
                  onClick={() => router.push('/chat/document')}
                  className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-md text-white font-semibold py-3 shadow-lg hover:shadow-xl transition-all border border-white/40"
                >
                  Start Document Chat
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </CardContent>
            </Card>

            {/* Chat with Company Policy */}
            <Card className="hover:shadow-2xl transition-all duration-300 cursor-pointer group border border-white/30 bg-white/10 backdrop-blur-md hover:bg-white/20">
              <CardHeader>
                <div className="flex items-center justify-center mb-4">
                  <div className="p-6 bg-white/20 backdrop-blur-sm rounded-2xl group-hover:scale-110 transition-transform shadow-lg border border-white/40">
                    <Building2 className="w-12 h-12 text-white" />
                  </div>
                </div>
                <CardTitle className="text-center text-3xl font-bold text-white drop-shadow-lg">
                  Chat with Company Policy
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-100 mb-8 text-lg leading-relaxed">
                  Query all company policies and documents at once to get comprehensive, policy-aligned answers.
                </p>
                <Button 
                  onClick={() => router.push('/chat/policy')}
                  className="w-full bg-white/20 hover:bg-white/30 backdrop-blur-md text-white font-semibold py-3 shadow-lg hover:shadow-xl transition-all border border-white/40"
                >
                  Start Policy Chat
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="mt-12 max-w-5xl mx-auto">
            <h2 className="text-2xl font-bold text-white mb-6 text-center drop-shadow-lg">
              Quick Actions
            </h2>
            <div className="grid md:grid-cols-3 gap-4">
              <Button
                variant="outline"
                onClick={() => router.push('/documents')}
                className="h-auto py-4 bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-md"
              >
                <div className="text-center">
                  <FileText className="w-6 h-6 mx-auto mb-2" />
                  <div className="font-semibold">Manage Documents</div>
                  <div className="text-xs text-gray-200">Upload & organize</div>
                </div>
              </Button>
              
              <Button
                variant="outline"
                onClick={() => router.push('/users')}
                className="h-auto py-4 bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-md"
              >
                <div className="text-center">
                  <Users className="w-6 h-6 mx-auto mb-2" />
                  <div className="font-semibold">Manage Users</div>
                  <div className="text-xs text-gray-200">Add & edit users</div>
                </div>
              </Button>
              
              <Button
                variant="outline"
                onClick={() => router.push('/settings')}
                className="h-auto py-4 bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-md"
              >
                <div className="text-center">
                  <Settings className="w-6 h-6 mx-auto mb-2" />
                  <div className="font-semibold">RAG Settings</div>
                  <div className="text-xs text-gray-200">Configure AI parameters</div>
                </div>
              </Button>
            </div>
          </div>
        </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
