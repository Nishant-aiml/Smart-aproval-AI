'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { dashboardApi, type Evaluation } from '@/lib/api';
import { useAuth } from './AuthProvider';
import { Calendar, Filter, Building2, GraduationCap, ChevronDown } from 'lucide-react';
import toast from 'react-hot-toast';

interface EvaluationSelectorProps {
  currentBatchId?: string;
  onEvaluationSelect?: (batchId: string) => void;
}

export default function EvaluationSelector({ currentBatchId, onEvaluationSelect }: EvaluationSelectorProps) {
  const router = useRouter();
  const { user } = useAuth();
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Filter states
  const [selectedYear, setSelectedYear] = useState<string>('');
  const [selectedMode, setSelectedMode] = useState<string>('');
  const [selectedDepartment, setSelectedDepartment] = useState<string>('');
  
  // Unique values for dropdowns
  const [availableYears, setAvailableYears] = useState<string[]>([]);
  const [availableModes, setAvailableModes] = useState<string[]>([]);
  const [availableDepartments, setAvailableDepartments] = useState<string[]>([]);

  useEffect(() => {
    loadEvaluations();
  }, [selectedYear, selectedMode, selectedDepartment]);

  const loadEvaluations = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (selectedYear) params.academic_year = selectedYear;
      if (selectedMode) params.mode = selectedMode;
      if (selectedDepartment) params.department_name = selectedDepartment;
      
      const data = await dashboardApi.listEvaluations(params);
      setEvaluations(data);
      
      // Extract unique values for filters
      const years = new Set<string>();
      const modes = new Set<string>();
      const departments = new Set<string>();
      
      data.forEach(evaluation => {
        if (evaluation.academic_year) years.add(evaluation.academic_year);
        if (evaluation.mode) modes.add(evaluation.mode);
        if (evaluation.department_name) departments.add(evaluation.department_name);
      });
      
      setAvailableYears(Array.from(years).sort().reverse());
      setAvailableModes(Array.from(modes).sort());
      setAvailableDepartments(Array.from(departments).sort());
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || 'Failed to load evaluations');
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluationClick = (batchId: string) => {
    if (onEvaluationSelect) {
      onEvaluationSelect(batchId);
    } else {
      router.push(`/dashboard?batch_id=${batchId}`);
    }
  };

  const clearFilters = () => {
    setSelectedYear('');
    setSelectedMode('');
    setSelectedDepartment('');
  };

  const getModeColor = (mode: string) => {
    switch (mode.toLowerCase()) {
      case 'aicte': return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'nba': return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'naac': return 'bg-green-50 text-green-700 border-green-200';
      case 'nirf': return 'bg-orange-50 text-orange-700 border-orange-200';
      default: return 'bg-gray-50 text-gray-700 border-gray-200';
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-soft-lg p-6 mb-8 border border-gray-100">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary-light rounded-xl flex items-center justify-center">
            <Filter className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-800">Select Evaluation</h2>
            <p className="text-sm text-gray-500">Choose an academic year, mode, and department</p>
          </div>
        </div>
        {(selectedYear || selectedMode || selectedDepartment) && (
          <button
            onClick={clearFilters}
            className="text-sm text-primary hover:text-primary-dark font-medium"
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="grid md:grid-cols-3 gap-4 mb-6">
        {/* Academic Year Filter */}
        <div className="relative">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="w-4 h-4 inline mr-1" />
            Academic Year
          </label>
          <select
            value={selectedYear}
            onChange={(e) => setSelectedYear(e.target.value)}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent appearance-none bg-white"
          >
            <option value="">All Years</option>
            {availableYears.filter(Boolean).map((year, idx) => (
              <option key={`year-${year || idx}`} value={year}>{year}</option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-9 w-4 h-4 text-gray-400 pointer-events-none" />
        </div>

        {/* Mode Filter */}
        <div className="relative">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <GraduationCap className="w-4 h-4 inline mr-1" />
            Accreditation Mode
          </label>
          <select
            value={selectedMode}
            onChange={(e) => setSelectedMode(e.target.value)}
            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent appearance-none bg-white"
          >
            <option value="">All Modes</option>
            {availableModes.filter(Boolean).map((mode, idx) => (
              <option key={`mode-${mode || idx}`} value={mode}>{mode.toUpperCase()}</option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-9 w-4 h-4 text-gray-400 pointer-events-none" />
        </div>

        {/* Department Filter (only for institution users) */}
        {user?.role === 'institution' && (
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Building2 className="w-4 h-4 inline mr-1" />
              Department
            </label>
            <select
              value={selectedDepartment}
              onChange={(e) => setSelectedDepartment(e.target.value)}
              className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent appearance-none bg-white"
            >
              <option value="">All Departments</option>
              {availableDepartments.filter(Boolean).map((dept, idx) => (
                <option key={`dept-${dept || idx}`} value={dept}>{dept}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-9 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        )}
      </div>

      {/* Evaluations List */}
      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent mx-auto"></div>
          <p className="text-gray-500 mt-2">Loading evaluations...</p>
        </div>
      ) : evaluations.length === 0 ? (
        <div className="text-center py-8 bg-gray-50 rounded-xl border border-gray-200">
          <p className="text-gray-500">No evaluations found</p>
          <p className="text-sm text-gray-400 mt-1">Try adjusting your filters or create a new evaluation</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {evaluations.map((evaluation, idx) => (
            <div
              key={evaluation.batch_id || `eval-${idx}`}
              onClick={() => handleEvaluationClick(evaluation.batch_id)}
              className={`p-4 rounded-xl border-2 cursor-pointer transition-all hover:shadow-md ${
                currentBatchId === evaluation.batch_id
                  ? 'border-primary bg-primary-50'
                  : 'border-gray-200 bg-white hover:border-primary/50'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 rounded-lg text-xs font-semibold border ${getModeColor(evaluation.mode)}`}>
                      {evaluation.mode.toUpperCase()}
                    </span>
                    {evaluation.overall_score !== null && (
                      <span className="text-xs font-medium text-gray-500">
                        Score: {evaluation.overall_score.toFixed(1)}
                      </span>
                    )}
                  </div>
                  {evaluation.academic_year && (
                    <p className="text-sm font-medium text-gray-700 mb-1">
                      {evaluation.academic_year}
                    </p>
                  )}
                  {evaluation.department_name && (
                    <p className="text-xs text-gray-500 mb-1">
                      {evaluation.department_name}
                    </p>
                  )}
                  {evaluation.institution_name && (
                    <p className="text-xs text-gray-400">
                      {evaluation.institution_name}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{evaluation.total_documents} documents</span>
                {currentBatchId === evaluation.batch_id && (
                  <span className="text-primary font-medium">Current</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

