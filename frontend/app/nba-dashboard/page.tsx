'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Award, CheckCircle, AlertCircle, TrendingUp, XCircle, AlertTriangle, HelpCircle } from 'lucide-react';
import ProtectedRoute from '@/components/ProtectedRoute';
import dynamic from 'next/dynamic';

// Lazy load chatbot
const Chatbot = dynamic(() => import('@/components/Chatbot'), {
    loading: () => null,
    ssr: false,
});

// NBA API base
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '/api';

interface POAttainment {
    po_id: string;
    po_name: string;
    direct_attainment: number | null;
    indirect_attainment: number | null;
    final_attainment: number | null;
    status: string;
    has_evidence: boolean;
    formula_used?: string;
}

interface PSOAttainment {
    pso_id: string;
    pso_name: string;
    direct_attainment?: number | null;
    indirect_attainment?: number | null;
    final_attainment: number | null;
    status: string;
}

interface GapAnalysisItem {
    po_id: string;
    po_name?: string;
    current_value: number | null;
    target_value: number;
    gap: number | null;
    recommendation: string;
    severity?: string;
}

interface NBADashboardData {
    batch_id: string;
    institution_name?: string | null;
    program_name?: string | null;
    batch_status?: {
        is_valid: boolean;
        invalid_reason?: string;
    };
    po_attainments: POAttainment[];
    pso_attainments: PSOAttainment[];
    total_courses?: number;
    total_cos?: number;
    attained_pos: number;
    partially_attained_pos: number;
    not_attained_pos: number;
    attainment_target?: number | null;
    average_po_attainment: number | null;
    gap_analysis: GapAnalysisItem[];
    improvement_actions?: any[];
}

function NBADashboardContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const batchId = searchParams.get('batch_id');

    const [loading, setLoading] = useState(true);
    const [data, setData] = useState<NBADashboardData | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [isInvalid, setIsInvalid] = useState(false);
    const [invalidReason, setInvalidReason] = useState<string>('');

    useEffect(() => {
        const fetchData = async () => {
            if (!batchId) return;

            try {
                // Fetch NBA dashboard data from REAL API - ABSOLUTELY NO FALLBACK
                const response = await fetch(`${API_BASE}/nba/${batchId}/dashboard`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('firebase_token') || ''}`
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));

                    // Check for specific invalid batch errors
                    if (response.status === 400 && errorData.detail?.includes('invalid')) {
                        setIsInvalid(true);
                        setInvalidReason(errorData.detail || 'NBA batch is invalid');
                        setLoading(false);
                        return;
                    }

                    throw new Error(errorData.detail || `Failed to load NBA dashboard (${response.status})`);
                }

                const result = await response.json();

                // Check if batch is marked invalid in response
                if (result.batch_status && !result.batch_status.is_valid) {
                    setIsInvalid(true);
                    setInvalidReason(result.batch_status.invalid_reason || 'NBA batch has insufficient data');
                    setLoading(false);
                    return;
                }

                // Check for completely missing PO data
                const hasAnyPOData = result.po_attainments?.some(
                    (po: POAttainment) => po.final_attainment !== null || po.has_evidence
                );

                if (!hasAnyPOData && result.po_attainments?.length > 0) {
                    setIsInvalid(true);
                    setInvalidReason('No PO attainment data extracted from documents. Please upload CO definitions, CO-PO mapping, and student attainment data.');
                    setData(result); // Still set data for partial display
                    setLoading(false);
                    return;
                }

                setData(result);
            } catch (err) {
                console.error('Error fetching NBA data:', err);
                setError(err instanceof Error ? err.message : 'Failed to load NBA dashboard');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [batchId]);

    // Trigger chatbot to explain a PO
    const explainPO = (poId: string) => {
        const chatbotButton = document.querySelector('[aria-label="Open AI Assistant"]') as HTMLButtonElement;
        if (chatbotButton) {
            chatbotButton.click();
            setTimeout(() => {
                const chatbotInput = document.querySelector('input[placeholder="Ask a question..."]') as HTMLInputElement;
                if (chatbotInput) {
                    chatbotInput.value = `Explain ${poId} attainment for batch ${batchId}`;
                    chatbotInput.dispatchEvent(new Event('input', { bubbles: true }));
                    const sendButton = chatbotInput.nextElementSibling as HTMLButtonElement;
                    if (sendButton) {
                        setTimeout(() => sendButton.click(), 100);
                    }
                }
            }, 500);
        }
    };

    // Get status color for attainment
    const getStatusColor = (status: string) => {
        const s = status.toLowerCase().replace(/_/g, ' ');
        if (s === 'attained') return 'bg-green-100 text-green-800 border-green-200';
        if (s.includes('partial')) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        if (s.includes('not attained')) return 'bg-red-100 text-red-800 border-red-200';
        if (s.includes('insufficient')) return 'bg-gray-100 text-gray-600 border-gray-300';
        return 'bg-gray-100 text-gray-800 border-gray-200';
    };

    // Render value or "Insufficient Evidence"
    const renderValue = (value: number | null | undefined) => {
        if (value === null || value === undefined) {
            return <span className="text-gray-400 italic text-sm">Insufficient Evidence</span>;
        }
        return <span className="font-bold">{value.toFixed(1)}%</span>;
    };

    if (!batchId) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center bg-white rounded-3xl shadow-soft-lg p-12 max-w-md">
                    <Award className="w-16 h-16 text-secondary mx-auto mb-6" />
                    <p className="text-gray-600 mb-6">No batch selected. Please start from the home page.</p>
                    <button onClick={() => router.push('/')} className="btn-primary">Go to Home</button>
                </div>
            </div>
        );
    }

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-3 border-secondary border-t-transparent mx-auto mb-4" />
                    <p className="text-gray-600">Loading NBA Dashboard...</p>
                </div>
            </div>
        );
    }

    // ⚠️ FAIL LOUDLY: Invalid batch - show prominent error panel
    if (isInvalid) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 py-12">
                <div className="container mx-auto px-4 max-w-3xl">
                    <div className="bg-white rounded-3xl shadow-2xl border-4 border-red-400 p-8">
                        {/* Giant Error Icon */}
                        <div className="text-center mb-8">
                            <div className="inline-flex items-center justify-center w-24 h-24 bg-red-100 rounded-full mb-6">
                                <XCircle className="w-16 h-16 text-red-600" />
                            </div>
                            <h1 className="text-3xl font-bold text-red-800 mb-2">❌ NBA Evaluation Failed</h1>
                            <p className="text-xl text-red-600">Data Insufficient for Accreditation Analysis</p>
                        </div>

                        {/* Error Details */}
                        <div className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 mb-8">
                            <h2 className="font-bold text-red-800 mb-3 flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5" />
                                Reason for Failure
                            </h2>
                            <p className="text-red-700 text-lg">{invalidReason}</p>
                        </div>

                        {/* What's Missing */}
                        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6 mb-8">
                            <h2 className="font-bold text-orange-800 mb-3">Required Documents for NBA Mode:</h2>
                            <ul className="space-y-2 text-orange-700">
                                <li className="flex items-center gap-2">
                                    <XCircle className="w-4 h-4 text-red-500" />
                                    CO Definitions (Course Outcome statements)
                                </li>
                                <li className="flex items-center gap-2">
                                    <XCircle className="w-4 h-4 text-red-500" />
                                    CO-PO Mapping Table (with strength 1,2,3)
                                </li>
                                <li className="flex items-center gap-2">
                                    <XCircle className="w-4 h-4 text-red-500" />
                                    Student Attainment Data (marks per CO)
                                </li>
                                <li className="flex items-center gap-2 text-orange-500">
                                    <HelpCircle className="w-4 h-4" />
                                    Optional: ATR, Indirect Assessment
                                </li>
                            </ul>
                        </div>

                        {/* Action */}
                        <div className="text-center">
                            <p className="text-gray-600 mb-4">Upload the required NBA documents and reprocess this batch.</p>
                            <div className="flex justify-center gap-4">
                                <button
                                    onClick={() => router.push('/batches')}
                                    className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors"
                                >
                                    Back to Batches
                                </button>
                                <button
                                    onClick={() => router.push('/')}
                                    className="px-6 py-3 bg-secondary text-white rounded-xl hover:bg-secondary-dark transition-colors"
                                >
                                    Upload New Documents
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center bg-white rounded-3xl shadow-soft-lg p-12 max-w-md">
                    <XCircle className="w-16 h-16 text-red-400 mx-auto mb-6" />
                    <h2 className="text-xl font-bold text-red-800 mb-2">Error Loading Dashboard</h2>
                    <p className="text-red-600 mb-6">{error}</p>
                    <button onClick={() => router.push('/batches')} className="btn-primary">Back to Batches</button>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <div className="text-center bg-white rounded-3xl shadow-soft-lg p-12 max-w-md">
                    <AlertTriangle className="w-16 h-16 text-orange-400 mx-auto mb-6" />
                    <p className="text-gray-600 mb-6">No data available for this batch.</p>
                    <button onClick={() => router.push('/batches')} className="btn-primary">Back to Batches</button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-soft py-12">
            <div className="container mx-auto px-4 max-w-7xl">
                {/* Header */}
                <div className="text-center mb-12">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full shadow-soft mb-4 border border-secondary-100">
                        <Award className="w-4 h-4 text-secondary" />
                        <span className="text-sm font-medium text-secondary-dark">NBA Accreditation (OBE)</span>
                    </div>
                    <h1 className="text-4xl font-bold text-gray-800 mb-3">
                        {data.institution_name || 'NBA Dashboard'}
                    </h1>
                    <p className="text-gray-600">{data.program_name || 'Program Outcomes Evaluation'}</p>
                    <p className="text-sm text-gray-400 mt-2">Batch: {batchId}</p>
                </div>

                {/* Summary Cards */}
                <div className="grid md:grid-cols-4 gap-6 mb-8">
                    <div className="bg-white rounded-2xl shadow-soft p-6">
                        <h3 className="text-sm font-medium text-gray-500 mb-2">Average PO Attainment</h3>
                        <div className="text-3xl font-bold text-secondary">
                            {data.average_po_attainment !== null ? `${data.average_po_attainment.toFixed(1)}%` :
                                <span className="text-lg text-gray-400">No Data</span>}
                        </div>
                    </div>
                    <div className="bg-green-50 rounded-2xl shadow-soft p-6 border border-green-100">
                        <h3 className="text-sm font-medium text-green-600 mb-2">Attained (≥70%)</h3>
                        <div className="text-3xl font-bold text-green-700">{data.attained_pos}</div>
                    </div>
                    <div className="bg-yellow-50 rounded-2xl shadow-soft p-6 border border-yellow-100">
                        <h3 className="text-sm font-medium text-yellow-600 mb-2">Partially (50-69%)</h3>
                        <div className="text-3xl font-bold text-yellow-700">{data.partially_attained_pos}</div>
                    </div>
                    <div className="bg-red-50 rounded-2xl shadow-soft p-6 border border-red-100">
                        <h3 className="text-sm font-medium text-red-600 mb-2">Not Attained (&lt;50%)</h3>
                        <div className="text-3xl font-bold text-red-700">{data.not_attained_pos}</div>
                    </div>
                </div>

                {/* PO Attainment Table - REAL DATA ONLY */}
                <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8">
                    <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-secondary" />
                        Program Outcomes (PO1-PO12) - Real Extracted Data
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b-2 border-gray-100">
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">PO</th>
                                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Description</th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Direct</th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Indirect</th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Final</th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Status</th>
                                    <th className="text-center py-3 px-4 font-semibold text-gray-700">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.po_attainments.map((po) => (
                                    <tr key={po.po_id} className="border-b border-gray-50 hover:bg-gray-50">
                                        <td className="py-3 px-4 font-medium text-secondary">{po.po_id}</td>
                                        <td className="py-3 px-4 text-sm text-gray-600 max-w-xs">{po.po_name}</td>
                                        <td className="py-3 px-4 text-center">
                                            {renderValue(po.direct_attainment)}
                                        </td>
                                        <td className="py-3 px-4 text-center">
                                            {renderValue(po.indirect_attainment)}
                                        </td>
                                        <td className="py-3 px-4 text-center text-lg">
                                            {renderValue(po.final_attainment)}
                                        </td>
                                        <td className="py-3 px-4 text-center">
                                            <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(po.status)}`}>
                                                {po.status.replace(/_/g, ' ')}
                                            </span>
                                        </td>
                                        <td className="py-3 px-4 text-center">
                                            <button
                                                onClick={() => explainPO(po.po_id)}
                                                className="px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-xs hover:bg-blue-100 font-medium"
                                                title="Ask chatbot to explain this PO"
                                            >
                                                💬 Explain
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* PSO Attainment Table */}
                {data.pso_attainments && data.pso_attainments.length > 0 && (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8">
                        <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                            <Award className="w-5 h-5 text-purple-600" />
                            Program Specific Outcomes (PSO)
                        </h2>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead>
                                    <tr className="border-b-2 border-gray-100">
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">PSO</th>
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Description</th>
                                        <th className="text-center py-3 px-4 font-semibold text-gray-700">Attainment</th>
                                        <th className="text-center py-3 px-4 font-semibold text-gray-700">Status</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.pso_attainments.map((pso) => (
                                        <tr key={pso.pso_id} className="border-b border-gray-50 hover:bg-gray-50">
                                            <td className="py-3 px-4 font-medium text-purple-600">{pso.pso_id}</td>
                                            <td className="py-3 px-4 text-sm text-gray-600">{pso.pso_name}</td>
                                            <td className="py-3 px-4 text-center text-lg">
                                                {renderValue(pso.final_attainment)}
                                            </td>
                                            <td className="py-3 px-4 text-center">
                                                <span className={`px-3 py-1 rounded-full text-xs font-medium border ${getStatusColor(pso.status)}`}>
                                                    {pso.status.replace(/_/g, ' ')}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {/* Gap Analysis - From Backend Only */}
                {data.gap_analysis && data.gap_analysis.length > 0 && (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8">
                        <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
                            <AlertCircle className="w-5 h-5 text-orange-600" />
                            Gap Analysis (Backend-Computed)
                        </h2>
                        <div className="space-y-4">
                            {data.gap_analysis.map((item) => (
                                <div key={item.po_id} className="p-4 bg-orange-50 rounded-xl border border-orange-200">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="font-bold text-orange-800">{item.po_id}</span>
                                        <div className="flex items-center gap-4 text-sm">
                                            <span className="text-gray-600">
                                                Current: {item.current_value !== null ? `${item.current_value.toFixed(1)}%` : 'N/A'}
                                            </span>
                                            <span className="text-gray-600">Target: {item.target_value}%</span>
                                            <span className="font-medium text-red-600">
                                                Gap: {item.gap !== null ? `${item.gap.toFixed(1)}%` : 'N/A'}
                                            </span>
                                        </div>
                                    </div>
                                    <p className="text-sm text-orange-700">{item.recommendation}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Navigation */}
                <div className="flex justify-center gap-4">
                    <button
                        onClick={() => router.push('/batches')}
                        className="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors"
                    >
                        Back to Batches
                    </button>
                    <button
                        onClick={() => router.push(`/reports?batch_id=${batchId}`)}
                        className="px-6 py-3 bg-secondary text-white rounded-xl hover:bg-secondary-dark transition-colors"
                    >
                        Generate NBA Report
                    </button>
                </div>
            </div>

            {/* Chatbot */}
            <Chatbot batchId={batchId} currentPage="nba-dashboard" />
        </div>
    );
}

export default function NBADashboardPage() {
    return (
        <ProtectedRoute>
            <Suspense fallback={
                <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-3 border-secondary border-t-transparent" />
                </div>
            }>
                <NBADashboardContent />
            </Suspense>
        </ProtectedRoute>
    );
}
