'use client';

import { useState, useEffect } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import Navbar from '@/components/Navbar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { settingsApi, RAGSettings } from '@/lib/api';
import { Save, Settings as SettingsIcon } from 'lucide-react';

export default function SettingsPage() {
  const [settings, setSettings] = useState<RAGSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [formData, setFormData] = useState({
    chunk_size: 1000,
    chunk_overlap: 200,
    temperature: 0.7,
    top_p: 1.0,
    top_k: 4,
    model_name: 'gpt-3.5-turbo',
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsApi.getSettings();
      setSettings(data);
      setFormData({
        chunk_size: data.chunk_size,
        chunk_overlap: data.chunk_overlap,
        temperature: data.temperature,
        top_p: data.top_p,
        top_k: data.top_k,
        model_name: data.model_name,
      });
    } catch (error) {
      console.error('Error loading settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await settingsApi.updateSettings(formData);
      alert('Settings saved successfully!');
      loadSettings();
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Error saving settings');
    } finally {
      setIsSaving(false);
    }
  };

  const modelOptions = [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4-turbo-preview',
    'gpt-4o',
  ];

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50 dark:from-gray-900 dark:via-amber-900/20 dark:to-orange-900/20 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10 dark:opacity-5" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23F59E0B' fill-opacity='0.4' fill-rule='evenodd'/%3E%3C/svg%3E")`,
          backgroundSize: '100px 100px'
        }}></div>
        {/* Decorative Blobs */}
        <div className="absolute top-10 left-20 w-80 h-80 bg-amber-300 dark:bg-amber-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob"></div>
        <div className="absolute top-40 right-20 w-80 h-80 bg-orange-300 dark:bg-orange-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-20 left-1/3 w-80 h-80 bg-rose-300 dark:bg-rose-600 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        
        <div className="relative z-10">
        <Navbar activeTab="settings" />
        
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center p-3 bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl shadow-lg mb-4">
              <SettingsIcon className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent mb-2">
              RAG Settings
            </h1>
            <p className="text-gray-600 dark:text-gray-400">Configure your AI assistant parameters</p>
          </div>

          {isLoading ? (
            <div className="text-center py-12">Loading settings...</div>
          ) : (
            <div className="space-y-6">
              {/* Document Processing Settings */}
              <Card className="shadow-lg backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 border-0">
                <CardHeader>
                  <CardTitle>Document Processing</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Chunk Size
                      </label>
                      <Input
                        type="number"
                        value={formData.chunk_size}
                        onChange={(e) => setFormData({ ...formData, chunk_size: parseInt(e.target.value) })}
                        min="100"
                        max="5000"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Size of text chunks (100-5000 characters)
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Chunk Overlap
                      </label>
                      <Input
                        type="number"
                        value={formData.chunk_overlap}
                        onChange={(e) => setFormData({ ...formData, chunk_overlap: parseInt(e.target.value) })}
                        min="0"
                        max="1000"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Overlap between chunks (0-1000 characters)
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* LLM Settings */}
              <Card className="shadow-lg backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 border-0">
                <CardHeader>
                  <CardTitle>Language Model Configuration</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Model
                    </label>
                    <select
                      value={formData.model_name}
                      onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                      className="w-full h-10 rounded-md border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-950"
                    >
                      {modelOptions.map((model) => (
                        <option key={model} value={model}>
                          {model}
                        </option>
                      ))}
                    </select>
                    <p className="text-xs text-gray-500 mt-1">
                      OpenAI model to use for generating responses
                    </p>
                  </div>

                  <div className="grid md:grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Temperature
                      </label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.temperature}
                        onChange={(e) => setFormData({ ...formData, temperature: parseFloat(e.target.value) })}
                        min="0"
                        max="2"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Creativity level (0.0-2.0)
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Top P
                      </label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.top_p}
                        onChange={(e) => setFormData({ ...formData, top_p: parseFloat(e.target.value) })}
                        min="0"
                        max="1"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Nucleus sampling (0.0-1.0)
                      </p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">
                        Top K
                      </label>
                      <Input
                        type="number"
                        value={formData.top_k}
                        onChange={(e) => setFormData({ ...formData, top_k: parseInt(e.target.value) })}
                        min="1"
                        max="20"
                      />
                      <p className="text-xs text-gray-500 mt-1">
                        Number of documents to retrieve (1-20)
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Save Button */}
              <div className="flex justify-end">
                <Button onClick={handleSave} disabled={isSaving} className="px-8 shadow-lg bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700">
                  <Save className="w-4 h-4 mr-2" />
                  {isSaving ? 'Saving...' : 'Save Settings'}
                </Button>
              </div>
            </div>
          )}
        </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
