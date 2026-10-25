'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/ProtectedRoute';
import EvaluationSelector from '@/components/EvaluationSelector';
import { dashboardApi, type ForecastResponse } from '@/lib/api';
import toast from 'react-hot-toast';
import {
    ArrowLeft, RefreshCw, TrendingUp, TrendingDown,
    AlertTriangle, Target, ChevronDown
} from 'lucide-react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer, ReferenceLine
} from 'recharts';
import Chatbot from '@/components/Chatbot';

const KPI_OPTIONS = [
    { value: 'overall_score', label: 'Overall Score' },
    { value: 'fsr_score', label: 'FSR Score' },
    { value: 'infrastructure_score', label: 'Infrastructure Score' },
    { value: 'placement_index', label: 'Placement Index' },
    { value: 'lab_compliance_index', label: 'Lab Compliance Index' },
];

function ForecastPageContent() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const batchId = searchParams.get('batch_id') || '';
    const initialKpi = searchParams.get('kpi') || 'overall_score';

    const [forecast, setForecast] = useState<ForecastResponse | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [selectedKpi, setSelectedKpi] = useState(initialKpi);
    const [showSelector, setShowSelector] = useState(false);

    useEffect(() => {
        if (batchId && selectedKpi) {
            fetchForecast();
        } else {
            setLoading(false);
            setForecast(null);
        }
    }, [batchId, selectedKpi]);

    const fetchForecast = async () => {
        if (!batchId || !selectedKpi) return;

        setLoading(true);
        setError(null);
        try {
            const data = await dashboardApi.getForecast(batchId, selectedKpi);
            setForecast(data);

            if (data.insufficient_data || !data.has_forecast || !data.can_forecast) {
                toast.error(data.insufficient_data_reason || 'Insufficient data for forecast');
            }
        } catch (err: any) {
            console.error('Forecast API error:', err);
            const errorMsg = err.response?.data?.detail || 'Failed to load forecast';
            setError(errorMsg);
            toast.error(errorMsg);
            setForecast(null);
        } finally {
            setLoading(false);
        }
    };

    // Prepare chart data
    const chartData = forecast?.forecast ? forecast.forecast.map(point => ({
        year: point.year,
        predicted: point.predicted_value,
        lower: point.lower_bound,
        upper: point.upper_bound,
    })) : [];

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                <RefreshCw className="w-8 h-8 text-primary animate-spin" />
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
                            <h1 className="text-3xl font-bold text-gray-800">KPI Forecast</h1>
                            <p className="text-gray-600">Predict future performance based on historical trends</p>
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
                                router.push(`/forecast?batch_id=${id}&kpi=${selectedKpi}`);
                            }}
                        />
                    </div>
                )}

                {/* No Batch Selected Banner */}
                {!batchId && (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8 border border-gray-100">
                        <div className="text-center max-w-md mx-auto mb-6">
                            <Target className="w-12 h-12 text-primary mx-auto mb-3" />
                            <h2 className="text-xl font-bold text-gray-800 mb-2">Select an Evaluation to Forecast</h2>
                            <p className="text-gray-600">
                                Choose an evaluation batch from the list below to analyze multi-year KPI trajectories and projections.
                            </p>
                        </div>
                        <EvaluationSelector
                            onEvaluationSelect={(id) => router.push(`/forecast?batch_id=${id}&kpi=${selectedKpi}`)}
                        />
                    </div>
                )}

                {/* Error Banner when Batch is not found or fails */}
                {batchId && error && (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-8 mb-8 border border-red-100">
                        <div className="text-center max-w-md mx-auto mb-6">
                            <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-3" />
                            <h2 className="text-xl font-bold text-gray-800 mb-2">Evaluation Not Found</h2>
                            <p className="text-gray-600 mb-4">
                                The requested evaluation batch (<span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">{batchId}</span>) could not be retrieved. Please select an available evaluation below:
                            </p>
                            <button
                                onClick={() => router.push('/dashboard')}
                                className="px-5 py-2.5 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors font-medium text-sm shadow-soft"
                            >
                                Return to Dashboard
                            </button>
                        </div>
                        <div className="pt-4 border-t border-gray-100">
                            <h3 className="text-sm font-semibold text-gray-700 mb-3">Available Evaluations</h3>
                            <EvaluationSelector
                                onEvaluationSelect={(id) => router.push(`/forecast?batch_id=${id}&kpi=${selectedKpi}`)}
                            />
                        </div>
                    </div>
                )}

                {/* KPI Selector (only show if batchId is present and no 404 error) */}
                {batchId && !error && (
                    <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border border-gray-100">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Select KPI to Forecast</label>
                            <p className="text-xs text-gray-500">Forecast models use linear regression over multi-year records with 95% confidence intervals</p>
                        </div>
                        <select
                            value={selectedKpi}
                            onChange={(e) => setSelectedKpi(e.target.value)}
                            className="w-full sm:w-auto px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-primary focus:border-primary text-gray-800 font-medium"
                        >
                            {KPI_OPTIONS.map(opt => (
                                <option key={opt.value} value={opt.value}>{opt.label}</option>
                            ))}
                        </select>
                    </div>
                )}

                {/* Insufficient Data Banner */}
                {forecast && (forecast.insufficient_data || !forecast.has_forecast || !forecast.can_forecast) && (
                    <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6 mb-8 text-center">
                        <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-3" />
                        <h3 className="font-semibold text-amber-800 text-lg">Insufficient Data for Forecast</h3>
                        <p className="text-amber-700 mt-2">
                            {forecast.insufficient_data_reason || 'The uploaded documents do not contain sufficient multi-year data (minimum 3 years required) for forecasting.'}
                        </p>
                        <button
                            onClick={() => router.push(`/dashboard?batch_id=${batchId}`)}
                            className="mt-4 px-4 py-2 bg-primary text-white rounded-xl hover:bg-primary-dark transition-colors"
                        >
                            Go to Dashboard
                        </button>
                    </div>
                )}

                {/* Forecast Chart */}
                {forecast && forecast.forecast && forecast.forecast.length > 0 && (
                    <>
                        <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8 border border-gray-100">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-xl font-semibold text-gray-800">
                                    {KPI_OPTIONS.find(k => k.value === selectedKpi)?.label} Forecast
                                </h2>
                                {forecast.confidence_band && (
                                    <div className="flex items-center gap-2 bg-primary-50 px-3 py-1.5 rounded-lg border border-primary-100">
                                        <Target className="w-4 h-4 text-primary" />
                                        <span className="text-sm font-medium text-primary-dark">
                                            Confidence: {(forecast.confidence_band * 100).toFixed(0)}%
                                        </span>
                                    </div>
                                )}
                            </div>
                            <ResponsiveContainer width="100%" height={400}>
                                <LineChart data={chartData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                                    <XAxis dataKey="year" tick={{ fill: '#6B7280', fontSize: 12 }} />
                                    <YAxis domain={[0, 100]} tick={{ fill: '#6B7280', fontSize: 12 }} />
                                    <Tooltip />
                                    <Legend />
                                    <Line
                                        type="monotone"
                                        dataKey="predicted"
                                        stroke="#0D9488"
                                        strokeWidth={3}
                                        dot={{ r: 5 }}
                                        name="Predicted Value"
                                    />
                                    <Line
                                        type="monotone"
                                        dataKey="upper"
                                        stroke="#F97316"
                                        strokeWidth={2}
                                        strokeDasharray="5 5"
                                        dot={false}
                                        name="Upper Bound (95% CI)"
                                    />
                                    <Line
                                        type="monotone"
                                        dataKey="lower"
                                        stroke="#F97316"
                                        strokeWidth={2}
                                        strokeDasharray="5 5"
                                        dot={false}
                                        name="Lower Bound (95% CI)"
                                    />
                                </LineChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Forecast Details */}
                        {forecast.explanation && (
                            <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8 border border-gray-100">
                                <h3 className="text-lg font-semibold text-gray-800 mb-3">Forecast Explanation</h3>
                                <p className="text-gray-600 leading-relaxed">{forecast.explanation}</p>
                            </div>
                        )}

                        {/* Forecast Table */}
                        <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8 overflow-x-auto border border-gray-100">
                            <h3 className="text-lg font-semibold text-gray-800 mb-4">Forecast Values</h3>
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="border-b-2 border-gray-100">
                                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Year</th>
                                        <th className="text-right py-3 px-4 font-semibold text-gray-700">Predicted</th>
                                        <th className="text-right py-3 px-4 font-semibold text-gray-700">Lower Bound</th>
                                        <th className="text-right py-3 px-4 font-semibold text-gray-700">Upper Bound</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {forecast.forecast.map((point, idx) => (
                                        <tr key={idx} className="border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
                                            <td className="py-3 px-4 font-medium text-gray-800">{point.year}</td>
                                            <td className="py-3 px-4 text-right text-primary font-semibold">
                                                {point.predicted_value.toFixed(1)}
                                            </td>
                                            <td className="py-3 px-4 text-right text-gray-600">
                                                {point.lower_bound.toFixed(1)}
                                            </td>
                                            <td className="py-3 px-4 text-right text-gray-600">
                                                {point.upper_bound.toFixed(1)}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </>
                )}

                {/* Chatbot */}
                {batchId && <Chatbot batchId={batchId} currentPage="forecast" />}
            </div>
        </div>
    );
}

export default function ForecastPage() {
    return (
        <ProtectedRoute>
            <Suspense fallback={
                <div className="min-h-screen bg-gradient-soft flex items-center justify-center">
                    <RefreshCw className="w-8 h-8 text-primary animate-spin" />
                </div>
            }>
                <ForecastPageContent />
            </Suspense>
        </ProtectedRoute>
    );
}
