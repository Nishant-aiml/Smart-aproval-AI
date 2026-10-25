'use client';

import { useState, useEffect, Suspense } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { useSearchParams, useRouter } from 'next/navigation';
import { dashboardApi, type YearwiseTrendsResponse } from '@/lib/api';
import toast from 'react-hot-toast';
import {
    ArrowLeft, RefreshCw, TrendingUp, TrendingDown, Minus,
    AlertTriangle, ChevronDown
} from 'lucide-react';
import { useAuth } from '@/components/AuthProvider';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer, BarChart, Bar, Cell
} from 'recharts';
import Chatbot from '@/components/Chatbot';
import EvaluationSelector from '@/components/EvaluationSelector';

const KPI_COLORS: Record<string, string> = {
    'fsr_score': '#0D9488',
    'infrastructure_score': '#8B5CF6',
    'placement_index': '#F97316',
    'lab_compliance_index': '#EC4899',
    'overall_score': '#059669',
};

const KPI_NAMES: Record<string, string> = {
    'fsr_score': 'FSR Score',
    'infrastructure_score': 'Infrastructure',
    'placement_index': 'Placement',
    'lab_compliance_index': 'Lab Compliance',
    'overall_score': 'Overall',
};

const SlopeIcon = ({ slope }: { slope: number }) => {
    if (slope > 1) return <TrendingUp className="w-5 h-5 text-green-500" />;
    if (slope < -1) return <TrendingDown className="w-5 h-5 text-red-500" />;
    return <Minus className="w-5 h-5 text-gray-400" />;
};

function TrendsPageContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const batchId = searchParams.get('batch_id') || '';
    const { user } = useAuth();

    const [trends, setTrends] = useState<YearwiseTrendsResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [notFound, setNotFound] = useState(false);
    const [showSelector, setShowSelector] = useState(false);

    useEffect(() => {
        if (batchId) {
            fetchTrends();
        } else {
            // No batch ID - stop loading immediately
            setLoading(false);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [batchId]);

    const fetchTrends = async () => {
        try {
            setNotFound(false);
            const data = await dashboardApi.getTrends(batchId);
            setTrends(data);
        } catch (err: any) {
            console.error(err);
            if (err?.response?.status === 404) {
                setNotFound(true);
                toast.error('Evaluation not found. Please choose an available evaluation.');
            } else {
                toast.error('Failed to load trends');
            }
        } finally {
            setLoading(false);
        }
    };

    // Prepare multi-KPI line chart data
    const lineChartData = trends?.years_available && Array.isArray(trends.years_available) && trends.kpis_per_year
        ? trends.years_available.map(year => {
            const yearData = trends.kpis_per_year[String(year)] || {};
            return {
                year,
                ...Object.fromEntries(
                    Object.entries(yearData).map(([k, v]) => [KPI_NAMES[k] || k, v])
                ),
            };
        })
        : [];

    // Prepare slope bar chart data
    const slopeData = trends?.trends && typeof trends.trends === 'object'
        ? Object.entries(trends.trends).map(([kpi, info]) => {
            const trendInfo = info as { slope?: number };
            return {
                name: KPI_NAMES[kpi] || kpi,
                slope: trendInfo?.slope || 0,
                color: (trendInfo?.slope || 0) > 0 ? '#10B981' : (trendInfo?.slope || 0) < 0 ? '#EF4444' : '#9CA3AF',
            };
        })
        : [];

    // Show loading only for a reasonable time
    if (loading && batchId) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <RefreshCw className="w-8 h-8 text-primary animate-spin" />
            </div>
        );
    }

    // No batch ID or batch not found - show EvaluationSelector
    if (!batchId || notFound) {
        return (
            <div className="min-h-screen bg-gradient-soft py-8">
                <div className="container mx-auto px-4 max-w-6xl">
                    <div className="flex items-center gap-4 mb-8">
                        <button onClick={() => router.back()} className="p-2 bg-white rounded-xl shadow-soft hover:shadow-soft-lg transition-all">
                            <ArrowLeft className="w-5 h-5 text-gray-600" />
                        </button>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-800">KPI Trends Analysis</h1>
                            <p className="text-gray-600">Year-wise performance with slope and volatility</p>
                        </div>
                    </div>
                    {notFound && (
                        <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 mb-8 text-center">
                            <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto mb-2" />
                            <h3 className="font-semibold text-amber-800 text-lg">Evaluation Not Found</h3>
                            <p className="text-amber-700 text-sm mt-1">
                                The requested evaluation ({batchId}) was not found in the database. Please select an available evaluation below:
                            </p>
                        </div>
                    )}
                    <EvaluationSelector onEvaluationSelect={(id) => router.push(`/trends?batch_id=${id}`)} />
                </div>
            </div>
        );
    }


    return (
        <div className="min-h-screen bg-gradient-soft py-8">
            <div className="container mx-auto px-4 max-w-6xl">
                {/* Header */}
                <div className="flex items-center justify-between gap-4 mb-8">
                    <div className="flex items-center gap-4">
                        <button onClick={() => router.back()} className="p-2 bg-white rounded-xl shadow-soft hover:shadow-soft-lg transition-all">
                            <ArrowLeft className="w-5 h-5 text-gray-600" />
                        </button>
                        <div>
                            <h1 className="text-3xl font-bold text-gray-800">KPI Trends Analysis</h1>
                            <p className="text-gray-600">Year-wise performance with slope and volatility</p>
                        </div>
                    </div>
                    {batchId && (
                        <button
                            onClick={() => setShowSelector(!showSelector)}
                            className="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm font-medium text-gray-700 shadow-soft hover:shadow-soft-lg transition-all"
                        >
                            Change Evaluation
                            <ChevronDown className={`w-4 h-4 transition-transform ${showSelector ? 'rotate-180' : ''}`} />
                        </button>
                    )}
                </div>

                {/* Collapsible Evaluation Selector */}
                {showSelector && (
                    <div className="mb-8">
                        <EvaluationSelector
                            currentBatchId={batchId}
                            onEvaluationSelect={(id) => {
                                setShowSelector(false);
                                router.push(`/trends?batch_id=${id}`);
                            }}
                        />
                    </div>
                )}

                {/* No Historical Data Banner */}
                {(!trends || !trends.has_historical_data || (trends as any).insufficient_data) && (
                    <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 mb-8 text-center">
                        <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-3" />
                        <h3 className="font-semibold text-amber-800 text-lg">Insufficient Data for Trend Analysis</h3>
                        <p className="text-amber-700 mt-2">
                            {!trends
                                ? 'Trend data is not available. Please ensure the batch processing is complete.'
                                : (trends as any).insufficient_data_reason
                                    ? (trends as any).insufficient_data_reason
                                    : 'The uploaded documents do not contain sufficient multi-year data (minimum 3 years required) for trend analysis.'}
                        </p>
                        {!trends && (
                            <button
                                onClick={() => router.push(`/dashboard?batch_id=${batchId}`)}
                                className="mt-4 px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors"
                            >
                                Go to Dashboard
                            </button>
                        )}
                    </div>
                )}

                {/* Year Summary */}
                {trends && trends.has_historical_data && trends.years_available && trends.years_available.length >= 2 && (
                    <>
                        <div className="grid md:grid-cols-4 gap-4 mb-8">
                            <div className="bg-white rounded-2xl p-4 shadow-soft">
                                <p className="text-sm text-gray-500">Years Found</p>
                                <p className="text-2xl font-bold text-primary">{trends.years_available.length}</p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 shadow-soft">
                                <p className="text-sm text-gray-500">First Year</p>
                                <p className="text-2xl font-bold text-gray-800">{trends.years_available[0]}</p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 shadow-soft">
                                <p className="text-sm text-gray-500">Latest Year</p>
                                <p className="text-2xl font-bold text-gray-800">{trends.years_available[trends.years_available.length - 1]}</p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 shadow-soft">
                                <p className="text-sm text-gray-500">Data Points</p>
                                <p className="text-2xl font-bold text-primary">
                                    {Object.values(trends.trends).reduce((sum, t) => sum + t.data_points, 0)}
                                </p>
                            </div>
                        </div>

                        {/* Multi-KPI Line Chart */}
                        {lineChartData.length > 0 && (
                            <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8">
                                <h2 className="text-xl font-semibold text-gray-800 mb-4">KPI Trends Over Time</h2>
                                <ResponsiveContainer width="100%" height={400}>
                                    <LineChart data={lineChartData}>
                                        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                                        <XAxis dataKey="year" tick={{ fill: '#6B7280', fontSize: 12 }} />
                                        <YAxis domain={[0, 100]} tick={{ fill: '#6B7280', fontSize: 12 }} />
                                        <Tooltip />
                                        <Legend />
                                        {Object.entries(KPI_COLORS).map(([kpi, color]) => (
                                            <Line
                                                key={kpi}
                                                type="monotone"
                                                dataKey={KPI_NAMES[kpi]}
                                                stroke={color}
                                                strokeWidth={2}
                                                dot={{ r: 4 }}
                                                connectNulls
                                            />
                                        ))}
                                    </LineChart>
                                </ResponsiveContainer>
                            </div>
                        )}

                        {/* Slope Indicator Bars */}
                        <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8">
                            <h2 className="text-xl font-semibold text-gray-800 mb-4">Annual Growth Rate Per KPI</h2>
                            <ResponsiveContainer width="100%" height={250}>
                                <BarChart data={slopeData} layout="vertical">
                                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                                    <XAxis type="number" domain={[-10, 10]} tickFormatter={v => `${v > 0 ? '+' : ''}${v}`} />
                                    <YAxis dataKey="name" type="category" width={120} tick={{ fontSize: 12 }} />
                                    <Tooltip formatter={v => [`${Number(v) > 0 ? '+' : ''}${v}/year`, 'Slope']} />
                                    <Bar dataKey="slope" radius={[0, 4, 4, 0]}>
                                        {slopeData.map((entry, idx) => (
                                            <Cell key={idx} fill={entry.color} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Trend Insights Cards */}
                        <div className="bg-white rounded-3xl shadow-soft-lg p-6">
                            <h2 className="text-xl font-semibold text-gray-800 mb-4">Trend Insights</h2>
                            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {Object.entries(trends.trends).map(([kpi, info]) => (
                                    <div
                                        key={kpi}
                                        className={`p-4 rounded-2xl border ${info.slope > 1 ? 'bg-green-50 border-green-200' :
                                            info.slope < -1 ? 'bg-red-50 border-red-200' :
                                                'bg-gray-50 border-gray-200'
                                            }`}
                                    >
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="font-semibold text-gray-800">{KPI_NAMES[kpi] || kpi}</span>
                                            <SlopeIcon slope={info.slope} />
                                        </div>
                                        <p className="text-sm text-gray-600 mb-2">{info.insight}</p>
                                        <div className="flex justify-between text-xs text-gray-500">
                                            <span>Min: {info.min?.toFixed(1) || 'N/A'}</span>
                                            <span>Avg: {info.avg?.toFixed(1) || 'N/A'}</span>
                                            <span>Max: {info.max?.toFixed(1) || 'N/A'}</span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </>
                )}

                {/* Chatbot */}
                {batchId && <Chatbot batchId={batchId} currentPage="trends" />}
            </div>
        </div>
    );
}

export default function TrendsPage() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <RefreshCw className="w-8 h-8 text-primary animate-spin" />
            </div>
        }>
            <TrendsPageContent />
        </Suspense>
    );
}
