'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { processingApi, type ProcessingStatusResponse } from '@/lib/api';
import { CheckCircle, Loader2, FileSearch, Brain, Database, Shield, BarChart3, TrendingUp, ClipboardCheck, Sparkles } from 'lucide-react';

function ProcessingPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const batchId = searchParams.get('batch_id') || '';

  const [status, setStatus] = useState<ProcessingStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!batchId) {
      router.push('/');
      return;
    }

    let isFinished = false;
    let interval: NodeJS.Timeout;

    const pollStatus = async () => {
      if (isFinished) return;
      try {
        const statusData = await processingApi.getStatus(batchId);
        setStatus(statusData);
        setLoading(false);

        const isCompleted = statusData.status === 'completed' || statusData.current_stage === 'completed';
        const isFailed = statusData.status === 'failed' || statusData.current_stage === 'failed';
        
        if (isCompleted && !isFinished) {
          isFinished = true;
          if (interval) clearInterval(interval);
          setTimeout(() => {
            router.push(`/dashboard?batch_id=${batchId}`);
          }, 1500);
        } else if (isFailed) {
          isFinished = true;
          if (interval) clearInterval(interval);
          console.error('Processing failed:', statusData.errors);
        }
      } catch (error) {
        console.error('Error fetching status:', error);
        setLoading(false);
      }
    };

    pollStatus();
    interval = setInterval(pollStatus, 3000);

    return () => {
      isFinished = true;
      if (interval) clearInterval(interval);
    };
  }, [batchId, router]);

  const stages = [
    { key: 'docling_parsing', label: 'Document Parsing', description: 'Extracting text and structure', icon: FileSearch, progress: 10 },
    { key: 'ocr_fallback', label: 'OCR Processing', description: 'Scanning images for text', icon: FileSearch, progress: 15 },
    { key: 'section_extraction', label: 'Section Detection', description: 'Extracting relevant sections', icon: Database, progress: 20 },
    { key: 'classify_approval', label: 'Classification', description: 'Identifying document type', icon: Shield, progress: 25 },
    { key: 'snippet_extraction', label: 'Block Detection', description: 'Identifying information blocks', icon: Database, progress: 28 },
    { key: 'one_shot_extraction', label: 'AI Extraction', description: 'Processing with GPT model', icon: Brain, progress: 40 },
    { key: 'block_mapping', label: 'Block Mapping', description: 'Mapping to schema', icon: Database, progress: 50 },
    { key: 'storing_blocks', label: 'Data Storage', description: 'Saving extracted data', icon: Database, progress: 55 },
    { key: 'quality_check', label: 'Quality Check', description: 'Validating data quality', icon: Shield, progress: 60 },
    { key: 'sufficiency', label: 'Sufficiency Analysis', description: 'Checking document completeness', icon: ClipboardCheck, progress: 70 },
    { key: 'kpi_scoring', label: 'KPI Calculation', description: 'Computing performance metrics', icon: BarChart3, progress: 80 },
    { key: 'compliance', label: 'Compliance Check', description: 'Verifying regulations', icon: Shield, progress: 85 },
    { key: 'approval_classification', label: 'Approval Analysis', description: 'Classifying approval type', icon: ClipboardCheck, progress: 88 },
    { key: 'approval_readiness', label: 'Readiness Check', description: 'Checking approval readiness', icon: Shield, progress: 92 },
    { key: 'trend_analysis', label: 'Trend Analysis', description: 'Analyzing historical data', icon: TrendingUp, progress: 96 },
    { key: 'completed', label: 'Completed', description: 'Analysis complete!', icon: Sparkles, progress: 100 },
  ];

  // Use current_stage from backend, fallback to status
  const currentStage = status?.current_stage || status?.status || 'created';
  const currentStageIndex = stages.findIndex((s) => s.key === currentStage);
  const activeIndex = currentStageIndex >= 0 ? currentStageIndex : 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center">
            <Loader2 className="w-8 h-8 text-primary animate-spin" />
          </div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-soft py-12 relative overflow-hidden">
      {/* Decorative Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="shape-blob w-96 h-96 bg-primary-100 top-0 left-1/2 -translate-x-1/2 -translate-y-1/2" />
        <div className="shape-blob w-72 h-72 bg-secondary-50 bottom-0 right-0 translate-x-1/3 translate-y-1/3" />
      </div>

      <div className="container mx-auto px-4 max-w-4xl relative z-10">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-soft mb-4 border border-primary-100">
            <Brain className="w-4 h-4 text-primary animate-pulse" />
            <span className="text-sm font-medium text-primary-dark">AI Processing</span>
          </div>
          <h1 className="text-4xl font-bold text-gray-800 mb-3">
            Analyzing Documents
          </h1>
          <p className="text-gray-600">
            Please wait while we process your documents
          </p>
        </div>

        {/* Main Progress Card */}
        <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8">
          {/* Progress Header */}
          <div className="flex justify-between items-center mb-4">
            <div>
              <p className="text-lg font-semibold text-gray-800">
                {stages[activeIndex]?.label || 'Processing...'}
              </p>
              <p className="text-sm text-gray-500">
                {stages[activeIndex]?.description}
              </p>
            </div>
            <div className="text-right">
              <span className="text-3xl font-bold bg-gradient-to-r from-primary to-secondary-light bg-clip-text text-transparent">
                {status?.progress?.toFixed(0) || 0}%
              </span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden mb-2">
            <div
              className="h-full bg-gradient-to-r from-primary via-primary-light to-secondary-light rounded-full transition-all duration-500 ease-out"
              style={{ width: `${status?.progress || 0}%` }}
            />
          </div>
        </div>

        {/* Stages List */}
        <div className="bg-white rounded-3xl shadow-soft-lg p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Processing Stages</h2>
          <div className="space-y-3">
            {stages.map((stage, index) => {
              const isCompleted = index < activeIndex;
              const isCurrent = index === activeIndex;
              const StageIcon = stage.icon;

              return (
                <div
                  key={stage.key}
                  className={`flex items-center gap-4 p-4 rounded-2xl transition-all duration-300 ${isCurrent
                    ? 'bg-gradient-to-r from-primary-50 to-primary-100/50 ring-2 ring-primary ring-offset-2'
                    : isCompleted
                      ? 'bg-secondary-50'
                      : 'bg-gray-50'
                    }`}
                >
                  {/* Icon */}
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ${isCompleted
                    ? 'bg-secondary'
                    : isCurrent
                      ? 'bg-primary animate-pulse'
                      : 'bg-gray-200'
                    }`}>
                    {isCompleted ? (
                      <CheckCircle className="w-6 h-6 text-white" />
                    ) : isCurrent ? (
                      <Loader2 className="w-6 h-6 text-white animate-spin" />
                    ) : (
                      <StageIcon className="w-6 h-6 text-gray-400" />
                    )}
                  </div>

                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <p className={`font-medium ${isCurrent
                      ? 'text-primary-dark'
                      : isCompleted
                        ? 'text-secondary-dark'
                        : 'text-gray-500'
                      }`}>
                      {stage.label}
                    </p>
                    <p className="text-sm text-gray-500 truncate">
                      {stage.description}
                    </p>
                  </div>

                  {/* Progress Badge */}
                  <div className={`px-3 py-1 rounded-full text-xs font-medium ${isCompleted
                    ? 'bg-secondary text-white'
                    : isCurrent
                      ? 'bg-primary text-white'
                      : 'bg-gray-200 text-gray-500'
                    }`}>
                    {isCompleted ? '✓' : `${stage.progress}%`}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Status Messages */}
        {(status?.status === 'completed' || status?.current_stage === 'completed') && (
          <div className="mt-8 text-center animate-fade-in">
            <div className="inline-flex items-center gap-3 px-6 py-4 bg-secondary-50 border border-secondary rounded-2xl">
              <CheckCircle className="w-6 h-6 text-secondary" />
              <span className="text-secondary font-semibold">
                Processing completed! Redirecting to dashboard...
              </span>
            </div>
          </div>
        )}

        {(status?.status === 'failed' || status?.current_stage === 'failed') && (
          <div className="mt-8 text-center animate-fade-in">
            <div className="inline-flex items-center gap-3 px-6 py-4 bg-red-50 border border-red-300 rounded-2xl">
              <span className="text-red-600 font-semibold">
                Processing failed. Please try again.
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ProcessingPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-3 border-primary border-t-transparent" />
      </div>
    }>
      <ProcessingPageContent />
    </Suspense>
  );
}
