<template>
  <!--begin::Layout-->
  <div class="d-flex flex-column flex-xl-row">
    <!--begin::Sidebar-->
    <div class="flex-column flex-lg-row-auto w-100 w-xl-350px mb-10">
      <!--begin::Card-->
      <div class="card mb-5 mb-xl-8">
        <!--begin::Card body-->
        <div class="card-body pt-15">
          <!--begin::Summary-->
          <div class="d-flex flex-center flex-column mb-5">
            <!--begin::Avatar-->
            <div class="symbol symbol-100px symbol-circle mb-7">
              <div class="symbol-label bg-light-primary">
                <span class="text-primary fw-bold fs-1">{{ getContactInitials() }}</span>
              </div>
            </div>
            <!--end::Avatar-->

            <!--begin::Name-->
            <a
              href="#"
              class="fs-3 text-gray-800 text-hover-primary fw-bold mb-1"
            >
              {{ getContactName() }}
            </a>
            <!--end::Name-->

            <!--begin::Position-->
            <div class="fs-5 fw-semibold text-muted mb-6">{{ getContactType() }}</div>
            <!--end::Position-->

            <!--begin::Info-->
            <div class="d-flex flex-wrap flex-center">
              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getTotalTrips() }}</span>
                  <KTIcon icon-name="arrow-up" icon-class="fs-3 text-success" />
                </div>
                <div class="fw-semibold text-muted">Total Trips</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getTotalSpent() }}</span>
                </div>
                <div class="fw-semibold text-muted">Total Spent</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-50px">{{ getLastTripDate() }}</span>
                </div>
                <div class="fw-semibold text-muted">Last Trip</div>
              </div>
              <!--end::Stats-->
            </div>
            <!--end::Info-->
          </div>
          <!--end::Summary-->

          <!--begin::Details toggle-->
          <div class="d-flex flex-stack fs-4 py-3">
            <div
              class="fw-bold rotate collapsible"
              data-bs-toggle="collapse"
              href="#kt_contact_view_details"
              role="button"
              aria-expanded="false"
              aria-controls="kt_contact_view_details"
            >
              Details
              <span class="ms-2 rotate-180">
                <KTIcon icon-name="down" icon-class="fs-3" />
              </span>
            </div>

            <span
              data-bs-toggle="tooltip"
              data-bs-trigger="hover"
              title="Edit contact details"
            >
              <button class="btn btn-sm btn-light-primary">
                Edit
              </button>
            </span>
          </div>
          <!--end::Details toggle-->

          <div class="separator separator-dashed my-3"></div>

          <!--begin::Details content-->
          <div id="kt_contact_view_details" class="collapse show">
            <div class="py-5 fs-6">
              <!--begin::Badge-->
              <div :class="`badge badge-light-${getStatusColor()} d-inline`">{{ contact?.status || 'Active' }}</div>
              <!--end::Badge-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Contact ID</div>
              <div class="text-gray-600">{{ contact?.id || '-' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Email</div>
              <div class="text-gray-600">
                <a :href="`mailto:${contact?.email}`" class="text-gray-600 text-hover-primary">
                  {{ contact?.email || 'No email' }}
                </a>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Phone</div>
              <div class="text-gray-600">
                <a :href="`tel:${contact?.phone}`" class="text-gray-600 text-hover-primary">
                  {{ contact?.phone || 'No phone' }}
                </a>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Address</div>
              <div class="text-gray-600">
                {{ getFormattedAddress() }}
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Date of Birth</div>
              <div class="text-gray-600">{{ formatDate(contact?.date_of_birth) }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Emergency Contact</div>
              <div class="text-gray-600">{{ contact?.emergency_contact || 'Not provided' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Created</div>
              <div class="text-gray-600">{{ formatDate(contact?.created_on) }}</div>
              <!--end::Details item-->
            </div>
          </div>
          <!--end::Details content-->
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Card-->

      <!--begin::Medical Information (for patients)-->
      <div class="card mb-5 mb-xl-8" v-if="isPatient()">
        <!--begin::Card header-->
        <div class="card-header border-0">
          <div class="card-title">
            <h3 class="fw-bold m-0">Medical Information</h3>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-2">
          <div class="py-2">
            <!--begin::Medical Details-->
            <div class="fw-bold mt-3">Medical Condition</div>
            <div class="text-gray-600">{{ contact?.medical_condition || 'Not specified' }}</div>
            
            <div class="fw-bold mt-5">Allergies</div>
            <div class="text-gray-600">{{ contact?.allergies || 'None listed' }}</div>
            
            <div class="fw-bold mt-5">Medications</div>
            <div class="text-gray-600">{{ contact?.medications || 'None listed' }}</div>
            
            <div class="fw-bold mt-5">Insurance Provider</div>
            <div class="text-gray-600">{{ contact?.insurance_provider || 'Not provided' }}</div>
            
            <div class="fw-bold mt-5">Policy Number</div>
            <div class="text-gray-600">{{ contact?.insurance_policy || 'Not provided' }}</div>
            <!--end::Medical Details-->
          </div>
        </div>
        <!--end::Card body-->
      </div>
      <!--end::Medical Information-->
    </div>
    <!--end::Sidebar-->

    <!--begin::Content-->
    <div class="flex-lg-row-fluid ms-lg-15">
      <!--begin:::Tabs-->
      <ul
        class="nav nav-custom nav-tabs nav-line-tabs nav-line-tabs-2x border-0 fs-4 fw-semibold mb-8"
      >
        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4 active"
            data-bs-toggle="tab"
            href="#kt_contact_view_overview_tab"
          >
            Overview
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_contact_view_trips_tab"
          >
            Trips & Travel
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_contact_view_billing_tab"
          >
            Billing & Payments
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item">
          <a
            class="nav-link text-active-primary pb-4"
            data-bs-toggle="tab"
            href="#kt_contact_view_activity_tab"
          >
            Activity & Logs
          </a>
        </li>
        <!--end:::Tab item-->

        <!--begin:::Tab item-->
        <li class="nav-item ms-auto">
          <!--begin::Action menu-->
          <a
            href="#"
            class="btn btn-primary ps-7"
            data-kt-menu-trigger="click"
            data-kt-menu-attach="parent"
            data-kt-menu-placement="bottom-end"
          >
            Actions
            <KTIcon icon-name="down" icon-class="fs-2 me-0" />
          </a>
          <!--begin::Menu-->
          <div
            class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-200px py-4"
            data-kt-menu="true"
          >
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">Edit Contact</a>
            </div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">Create Trip</a>
            </div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">Generate Quote</a>
            </div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3">View Billing</a>
            </div>
            <div class="separator my-2"></div>
            <div class="menu-item px-3">
              <a href="#" class="menu-link px-3 text-danger">Deactivate</a>
            </div>
          </div>
          <!--end::Menu-->
        </li>
        <!--end:::Tab item-->
      </ul>
      <!--end:::Tabs-->

      <!--begin:::Tab content-->
      <div class="tab-content" id="myTabContent">
        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade show active"
          id="kt_contact_view_overview_tab"
          role="tabpanel"
        >
          <ContactOverview :contact="contact" :loading="loading" />
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_contact_view_trips_tab"
          role="tabpanel"
        >
          <ContactTrips :contact="contact" :loading="loading" />
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_contact_view_billing_tab"
          role="tabpanel"
        >
          <ContactBilling :contact="contact" :loading="loading" />
        </div>
        <!--end:::Tab pane-->

        <!--begin:::Tab pane-->
        <div
          class="tab-pane fade"
          id="kt_contact_view_activity_tab"
          role="tabpanel"
        >
          <ContactActivity :contact="contact" :loading="loading" />
        </div>
        <!--end:::Tab pane-->
      </div>
      <!--end:::Tab content-->
    </div>
    <!--end::Content-->
  </div>
  <!--end::Layout-->
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ApiService from "@/core/services/ApiService";
import ContactOverview from "@/components/contacts/cards/overview/ContactOverview.vue";
import ContactTrips from "@/components/contacts/cards/trips/ContactTrips.vue";
import ContactBilling from "@/components/contacts/cards/billing/ContactBilling.vue";
import ContactActivity from "@/components/contacts/cards/activity/ContactActivity.vue";

export default defineComponent({
  name: "contact-details",
  components: {
    ContactOverview,
    ContactTrips,
    ContactBilling,
    ContactActivity,
  },
  setup() {
    const route = useRoute();
    const contact = ref<any>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);

    const fetchContact = async () => {
      try {
        loading.value = true;
        error.value = null;
        const contactId = route.params.id as string;
        const contactType = route.params.type as string; // 'contacts', 'customers', 'patients'
        
        // Determine the correct endpoint based on type
        let endpoint = '';
        switch (contactType) {
          case 'patients':
            endpoint = `/patients/${contactId}/`;
            break;
          case 'customers':
            endpoint = `/customers/${contactId}/`;
            break;
          default:
            endpoint = `/contacts/${contactId}/`;
        }
        
        const response = await ApiService.get(endpoint);
        contact.value = { ...response.data, type: contactType };
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch contact details";
        console.error("Error fetching contact:", err);
      } finally {
        loading.value = false;
      }
    };

    const getContactInitials = (): string => {
      if (contact.value) {
        const first = contact.value.first_name?.charAt(0) || '';
        const last = contact.value.last_name?.charAt(0) || '';
        return (first + last).toUpperCase() || contact.value.email?.charAt(0).toUpperCase() || 'C';
      }
      return 'C';
    };

    const getContactName = (): string => {
      if (contact.value) {
        const first = contact.value.first_name || '';
        const last = contact.value.last_name || '';
        const name = `${first} ${last}`.trim();
        return name || contact.value.email || 'Unknown Contact';
      }
      return 'Loading...';
    };

    const getContactType = (): string => {
      const type = contact.value?.type || '';
      switch (type) {
        case 'patients': return 'Patient';
        case 'customers': return 'Customer';
        default: return 'Contact';
      }
    };

    const getTotalTrips = (): string => {
      return contact.value?.total_trips?.toString() || '0';
    };

    const getTotalSpent = (): string => {
      const amount = contact.value?.total_spent || 0;
      return `$${amount.toLocaleString()}`;
    };

    const getLastTripDate = (): string => {
      if (!contact.value?.last_trip_date) return 'Never';
      return new Date(contact.value.last_trip_date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      });
    };

    const getStatusColor = (): string => {
      const status = contact.value?.status?.toLowerCase();
      switch (status) {
        case 'active': return 'success';
        case 'inactive': return 'secondary';
        case 'suspended': return 'danger';
        default: return 'primary';
      }
    };

    const getFormattedAddress = (): string => {
      if (!contact.value) return 'No address provided';
      
      const parts = [
        contact.value.address,
        contact.value.city,
        contact.value.state,
        contact.value.zip_code,
        contact.value.country
      ].filter(Boolean);
      
      return parts.length > 0 ? parts.join(', ') : 'No address provided';
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'Not provided';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    const isPatient = (): boolean => {
      return contact.value?.type === 'patients';
    };

    onMounted(() => {
      fetchContact();
    });

    return {
      contact,
      loading,
      error,
      getContactInitials,
      getContactName,
      getContactType,
      getTotalTrips,
      getTotalSpent,
      getLastTripDate,
      getStatusColor,
      getFormattedAddress,
      formatDate,
      isPatient,
    };
  },
});
</script>