import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/core/services/ApiService";

export interface DashboardStats {
  trip_stats: {
    total: number;
    active: number;
    completed_30_days: number;
    types_breakdown: Array<{ type: string; count: number }>;
  };
  quote_stats: {
    total: number;
    pending: number;
    active: number;
    completed: number;
    statuses_breakdown: Array<{ status: string; count: number }>;
  };
  patient_stats: {
    total: number;
    active: number;
  };
  aircraft_stats: {
    total: number;
  };
  financial_stats: {
    total_revenue: number;
    pending_revenue: number;
  };
  recent_activity: {
    quotes: Array<{
      id: string;
      amount: number;
      status: string;
      created_on: string;
      patient_name: string;
    }>;
    trips: Array<{
      id: string;
      trip_number: string;
      type: string;
      status: string;
      created_on: string;
      estimated_departure: string | null;
    }>;
  };
}

export const useDashboardStore = defineStore("dashboard", () => {
  const stats = ref<DashboardStats | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Fetch dashboard statistics
   */
  async function fetchStats() {
    try {
      loading.value = true;
      error.value = null;
      
      const { data } = await ApiService.get("/dashboard/stats/");
      stats.value = data;
      
      return data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Failed to fetch dashboard stats";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Clear dashboard data
   */
  function clearStats() {
    stats.value = null;
    error.value = null;
  }

  /**
   * Format currency values
   */
  function formatCurrency(amount: number): string {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(amount);
  }

  /**
   * Format date values
   */
  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  /**
   * Format datetime values
   */
  function formatDateTime(dateString: string): string {
    return new Date(dateString).toLocaleString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  /**
   * Get status color for badges
   */
  function getStatusColor(status: string): string {
    const statusColors: Record<string, string> = {
      pending: "warning",
      active: "primary",
      completed: "success",
      cancelled: "danger",
      paid: "success",
      confirmed: "info",
      medical: "danger",
      charter: "primary",
      maintenance: "secondary",
    };
    
    return statusColors[status] || "secondary";
  }

  /**
   * Get completion percentage for quotes
   */
  function getQuoteCompletionPercentage(): number {
    if (!stats.value?.quote_stats) return 0;
    
    const { completed, total } = stats.value.quote_stats;
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  }

  /**
   * Get trip activity percentage (active trips vs total)
   */
  function getTripActivityPercentage(): number {
    if (!stats.value?.trip_stats) return 0;
    
    const { active, total } = stats.value.trip_stats;
    return total > 0 ? Math.round((active / total) * 100) : 0;
  }

  return {
    stats,
    loading,
    error,
    fetchStats,
    clearStats,
    formatCurrency,
    formatDate,
    formatDateTime,
    getStatusColor,
    getQuoteCompletionPercentage,
    getTripActivityPercentage,
  };
});