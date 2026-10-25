'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import {
    FolderOpen, ArrowLeft, BarChart3, Clock, CheckCircle,
    XCircle, AlertCircle, Loader2, FileText, TrendingUp, Play
} from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '@/components/AuthProvider';
import { batchApi } from '@/lib/api';

interface Batch {
    id: string;
    mode: string;
    status: 'pending' | 'processing' | 'completed' | 'failed';
    created_at: string;
    document_count: number;
    overall_score?: number;
    institution_name?: string | null;
}

export default function BatchesPage() {
    const router = useRouter();
    const { user } = useAuth();
    const [batches, setBatches] = useState<Batch[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBatches = async () => {
            try {
                const data = await batchApi.list();
                const rawList = Array.isArray(data) ? data : ((data as any).batches || []);
                const formatted: Batch[] = rawList.map((b: any) => ({
                    id: b.batch_id || b.id,
                    mode: b.mode ? b.mode.toUpperCase() : 'AICTE',
                    status: b.status || 'completed',
                    created_at: b.created_at || new Date().toISOString(),
                    document_count: b.total_documents ?? b.document_count ?? 0,
                    overall_score: b.overall_score,
                    institution_name: b.institution_name,
                }));
                setBatches(formatted);
            } catch (error) {
                console.error('Failed to fetch batches:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchBatches();
    }, []);

    const formatDate = (dateString: string) => {
        if (!dateString) return '';
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'completed':
                return <CheckCircle className="w-5 h-5 text-green-500" />;
            case 'processing':
                return <Loader2 className="w-5 h-5 text-primary animate-spin" />;
            case 'failed':
                return <XCircle className="w-5 h-5 text-red-500" />;
            default:
                return <Clock className="w-5 h-5 text-gray-400" />;
        }
    };

    const getStatusStyle = (status: string) => {
        switch (status) {
            case 'completed':
                return 'bg-green-100 text-green-700 border-green-200';
            case 'processing':
                return 'bg-primary-100 text-primary border-primary-200';
            case 'failed':
                return 'bg-red-100 text-red-700 border-red-200';
            default:
                return 'bg-gray-100 text-gray-700 border-gray-200';
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center animate-pulse">
                        <FolderOpen className="w-8 h-8 text-primary" />
                    </div>
                    <p className="text-gray-600">Loading evaluations...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-soft py-8">
            <div className="container mx-auto px-4 max-w-6xl">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => router.back()}
                            className="p-2 bg-white rounded-xl shadow-soft hover:shadow-soft-lg transition-all"
                        >
                            <ArrowLeft className="w-5 h-5 text-gray-600" />
                        </button>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-800">All Evaluations</h1>
                            <p className="text-gray-600">View and manage all your batch evaluations</p>
                        </div>
                    </div>
                    <Link
                        href="/"
                        className="px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors flex items-center gap-2"
                    >
                        <Play className="w-4 h-4" />
                        New Evaluation
                    </Link>
                </div>

                {/* Batches List */}
                {batches.length > 0 ? (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-6 border border-gray-100">
                        <div className="space-y-4">
                            {batches.map((batch, idx) => (
                                <div
                                    key={batch.id || `batch-${idx}`}
                                    className="flex items-center justify-between p-5 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors border border-gray-100"
                                >
                                    <div className="flex items-center gap-4">
                                        <div className="w-14 h-14 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center">
                                            <FolderOpen className="w-7 h-7 text-white" />
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <h3 className="font-semibold text-gray-800">
                                                    {batch.institution_name ? `${batch.institution_name} (${batch.mode})` : `${batch.mode} Evaluation`}
                                                </h3>
                                                <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${getStatusStyle(batch.status)}`}>
                                                    {batch.status}
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-4 text-sm text-gray-500">
                                                <span className="flex items-center gap-1">
                                                    <Clock className="w-4 h-4" />
                                                    {formatDate(batch.created_at)}
                                                </span>
                                                <span className="flex items-center gap-1">
                                                    <FileText className="w-4 h-4" />
                                                    {batch.document_count} documents
                                                </span>
                                                {batch.overall_score && (
                                                    <span className="flex items-center gap-1 text-primary font-medium">
                                                        <TrendingUp className="w-4 h-4" />
                                                        Score: {batch.overall_score.toFixed(1)}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        {getStatusIcon(batch.status)}
                                        {batch.status === 'completed' ? (
                                            <Link
                                                href={`/dashboard?batch_id=${batch.id}`}
                                                className="px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors flex items-center gap-2"
                                            >
                                                <BarChart3 className="w-4 h-4" />
                                                View Dashboard
                                            </Link>
                                        ) : batch.status === 'processing' ? (
                                            <Link
                                                href={`/processing?batch_id=${batch.id}`}
                                                className="px-4 py-2 bg-primary-50 text-primary border border-primary rounded-xl hover:bg-primary-100 transition-colors flex items-center gap-2"
                                            >
                                                <Loader2 className="w-4 h-4" />
                                                View Progress
                                            </Link>
                                        ) : (
                                            <span className="px-4 py-2 text-gray-400">
                                                {batch.status === 'failed' ? 'Failed' : 'Pending'}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-12 text-center border border-gray-100">
                        <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h2 className="text-xl font-semibold text-gray-700 mb-2">No Evaluations Yet</h2>
                        <p className="text-gray-500 mb-6">
                            Start your first evaluation by uploading documents.
                        </p>
                        <Link
                            href="/"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors"
                        >
                            <Play className="w-5 h-5" />
                            Start New Evaluation
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );
}
