<template>
  <!--begin::Recent Quotes Widget-->
  <div class="card" :class="widgetClasses">
    <!--begin::Header-->
    <div class="card-header align-items-center border-0 mt-4">
      <h3 class="card-title align-items-start flex-column">
        <span class="fw-bold text-gray-900">Recent Quotes</span>
        <span class="text-muted mt-1 fw-semibold fs-7">{{ recentQuotes.length }} recent requests</span>
      </h3>

      <div class="card-toolbar">
        <button @click="viewAllQuotes" class="btn btn-sm btn-light">View All</button>
      </div>
    </div>
    <!--end::Header-->

    <!--begin::Body-->
    <div class="card-body pt-3">
      <template v-for="(quote, index) in recentQuotes" :key="quote.id">
        <!--begin::Item-->
        <div
          :class="{ 'mb-7': recentQuotes.length - 1 !== index }"
          class="d-flex align-items-sm-center"
        >
          <!--begin::Symbol-->
          <div class="symbol symbol-60px me-4">
            <div class="symbol-label bg-light-primary">
              <KTIcon icon-name="document" icon-class="text-primary fs-2x" />
            </div>
          </div>
          <!--end::Symbol-->

          <!--begin::Content-->
          <div class="d-flex flex-row-fluid flex-wrap align-items-center">
            <div class="flex-grow-1 me-2">
              <a
                @click.prevent="viewQuote(quote)"
                href="#"
                class="text-gray-800 fw-bold text-hover-primary fs-6"
              >{{ quote.quote_number || `Quote #${quote.id.slice(0, 8)}` }}</a>

              <div class="d-flex flex-column">
                <span class="text-muted fw-semibold fs-7">{{ getContactName(quote) }}</span>
                <span class="text-muted fw-semibold fs-8">{{ formatDate(quote.created_on) }}</span>
              </div>
            </div>

            <div class="d-flex flex-column align-items-end">
              <span
                :class="`badge badge-light-${getStatusColor(quote.status)} fs-8 fw-bold mb-1`"
              >{{ quote.status }}</span>
              <span class="text-gray-600 fw-semibold fs-7" v-if="quote.total_amount">
                ${{ parseFloat(quote.total_amount).toLocaleString() }}
              </span>
            </div>
          </div>
          <!--end::Content-->
        </div>
        <!--end::Item-->
      </template>

      <!-- Empty state -->
      <div v-if="recentQuotes.length === 0" class="text-center text-muted py-10">
        <KTIcon icon-name="document" icon-class="fs-3x text-muted mb-3" />
        <div class="fw-semibold">No recent quotes</div>
        <div class="fs-7">New quote requests will appear here</div>
      </div>
    </div>
    <!--end::Body-->
  </div>
  <!--end::Recent Quotes Widget-->
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";

interface Props {
  className?: string;
}

const props = defineProps<Props>();
const router = useRouter();

const recentQuotes = ref<any[]>([]);
const loading = ref(false);

const widgetClasses = props.className;

const fetchRecentQuotes = async () => {
  try {
    loading.value = true;
    const response = await ApiService.get("/quotes/?page_size=8");
    const allQuotes = response.data.results || response.data || [];
    
    // Sort by creation date (most recent first) and take first 8
    recentQuotes.value = allQuotes
      .sort((a: any, b: any) => {
        const aDate = new Date(a.created_on);
        const bDate = new Date(b.created_on);
        return bDate.getTime() - aDate.getTime();
      })
      .slice(0, 8);
  } catch (error) {
    console.error("Error fetching recent quotes:", error);
  } finally {
    loading.value = false;
  }
};

const viewQuote = (quote: any) => {
  router.push(`/admin/quotes/${quote.id}`);
};

const viewAllQuotes = () => {
  router.push('/admin/quotes');
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'pending': return 'warning';
    case 'approved': return 'success';
    case 'rejected': return 'danger';
    case 'draft': return 'secondary';
    case 'sent': return 'info';
    case 'accepted': return 'success';
    case 'expired': return 'dark';
    default: return 'primary';
  }
};

const getContactName = (quote: any): string => {
  if (quote.contact) {
    const first = quote.contact.first_name || '';
    const last = quote.contact.last_name || '';
    const name = `${first} ${last}`.trim();
    return name || quote.contact.business_name || quote.contact.email || 'Contact';
  }
  if (quote.patient?.info) {
    const first = quote.patient.info.first_name || '';
    const last = quote.patient.info.last_name || '';
    const name = `${first} ${last}`.trim();
    return name || quote.patient.info.email || 'Patient';
  }
  return 'Unknown Contact';
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'Unknown';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

onMounted(() => {
  fetchRecentQuotes();
});
</script>