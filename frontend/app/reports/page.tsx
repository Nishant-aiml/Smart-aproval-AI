'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FileText, Download, Calendar, ArrowLeft, BarChart3, AlertCircle } from 'lucide-react';
import Link from 'next/link';
import { useAuth } from '@/components/AuthProvider';

interface Report {
    id: string;
    batch_id: string;
    created_at: string;
    report_type: string;
    download_url: string;
    mode: string;
}

export default function ReportsPage() {
    const router = useRouter();
    const { user } = useAuth();
    const [reports, setReports] = useState<Report[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch only real reports from API - no demo mode
        const fetchReports = async () => {
            try {
                const response = await fetch('/api/reports/list', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('auth_token') || ''}`
                    }
                });
                if (response.ok) {
                    const data = await response.json();
                    setReports(data.reports || []);
                }
            } catch (error) {
                console.error('Failed to fetch reports:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchReports();
    }, []);

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center">
                    <div className="w-16 h-16 mx-auto mb-4 bg-primary-100 rounded-2xl flex items-center justify-center animate-pulse">
                        <FileText className="w-8 h-8 text-primary" />
                    </div>
                    <p className="text-gray-600">Loading reports...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-soft py-8">
            <div className="container mx-auto px-4 max-w-6xl">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <button
                        onClick={() => router.back()}
                        className="p-2 bg-white rounded-xl shadow-soft hover:shadow-soft-lg transition-all"
                    >
                        <ArrowLeft className="w-5 h-5 text-gray-600" />
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-800">Generated Reports</h1>
                        <p className="text-gray-600">Download and manage your evaluation reports</p>
                    </div>
                </div>

                {/* Reports List */}
                {reports.length > 0 ? (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-6 border border-gray-100">
                        <div className="space-y-4">
                            {reports.map((report) => (
                                <div
                                    key={report.id}
                                    className="flex items-center justify-between p-4 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-colors"
                                >
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                                            <FileText className="w-6 h-6 text-primary" />
                                        </div>
                                        <div>
                                            <h3 className="font-semibold text-gray-800">
                                                {report.mode} Report - {report.report_type}
                                            </h3>
                                            <div className="flex items-center gap-2 text-sm text-gray-500">
                                                <Calendar className="w-4 h-4" />
                                                {formatDate(report.created_at)}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <Link
                                            href={`/dashboard?batch_id=${report.batch_id}`}
                                            className="px-4 py-2 text-primary border border-primary rounded-xl hover:bg-primary-50 transition-colors flex items-center gap-2"
                                        >
                                            <BarChart3 className="w-4 h-4" />
                                            View Dashboard
                                        </Link>
                                        <button
                                            onClick={async () => {
                                                try {
                                                    // Use the backend API to generate and download report
                                                    const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '/api';

                                                    // First generate the report
                                                    const generateResponse = await fetch(`${API_BASE}/reports/generate`, {
                                                        method: 'POST',
                                                        headers: { 'Content-Type': 'application/json' },
                                                        body: JSON.stringify({
                                                            batch_id: report.batch_id,
                                                            include_evidence: true,
                                                            include_trends: true,
                                                            report_type: report.report_type
                                                        })
                                                    });

                                                    if (generateResponse.ok) {
                                                        const result = await generateResponse.json();

                                                        // Download the generated report
                                                        const downloadResponse = await fetch(`${API_BASE}/reports/download/${report.batch_id}`);
                                                        if (downloadResponse.ok) {
                                                            const blob = await downloadResponse.blob();
                                                            const url = window.URL.createObjectURL(blob);
                                                            const a = document.createElement('a');
                                                            a.href = url;
                                                            a.download = `${report.mode}_Report_${report.batch_id}.pdf`;
                                                            document.body.appendChild(a);
                                                            a.click();
                                                            window.URL.revokeObjectURL(url);
                                                            document.body.removeChild(a);
                                                        } else {
                                                            alert('Report generated but download failed. Please try again.');
                                                        }
                                                    } else {
                                                        const errorData = await generateResponse.json().catch(() => ({}));
                                                        alert(errorData.detail || 'Failed to generate report. Please try again.');
                                                    }
                                                } catch (error) {
                                                    console.error('Download error:', error);
                                                    alert('Failed to download report. Please ensure the backend is running.');
                                                }
                                            }}
                                            className="px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors flex items-center gap-2"
                                        >
                                            <Download className="w-4 h-4" />
                                            Download
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-12 text-center border border-gray-100">
                        <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                        <h2 className="text-xl font-semibold text-gray-700 mb-2">No Reports Generated Yet</h2>
                        <p className="text-gray-500 mb-6">
                            Reports are generated from the dashboard after processing documents.
                        </p>
                        <Link
                            href="/dashboard"
                            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors"
                        >
                            <BarChart3 className="w-5 h-5" />
                            Go to Dashboard
                        </Link>
                    </div>
                )}
            </div>
        </div>
    );
}
