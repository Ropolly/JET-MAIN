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

            <!--begin::Role Badges-->
            <div class="d-flex flex-wrap justify-content-center mb-6" v-if="contactRoles.length > 0">
              <span
                v-for="role in contactRoles"
                :key="role.type"
                :class="`badge badge-light-${role.color} fs-8 fw-bold me-2 mb-2`"
              >
                <i :class="`ki-duotone ${role.icon} fs-7 me-1`">
                  <span class="path1"></span>
                  <span class="path2"></span>
                  <span class="path3"></span>
                  <span v-if="role.icon === 'ki-people'" class="path4"></span>
                  <span v-if="role.icon === 'ki-people'" class="path5"></span>
                </i>
                {{ role.label }}
              </span>
            </div>
            <!--end::Role Badges-->

            <!--begin::Info-->
            <div class="d-flex flex-wrap flex-center" v-if="!isPatient()">
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
            <!--begin::Patient Info-->
            <div class="d-flex flex-wrap flex-center" v-else>
              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ getPatientAge() }}</span>
                </div>
                <div class="fw-semibold text-muted">Age</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mx-4 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ contact?.status || 'Unknown' }}</span>
                </div>
                <div class="fw-semibold text-muted">Status</div>
              </div>
              <!--end::Stats-->

              <!--begin::Stats-->
              <div
                class="border border-gray-300 border-dashed rounded py-3 px-3 mb-3"
              >
                <div class="fs-4 fw-bold text-gray-700">
                  <span class="w-75px">{{ formatDate(contact?.created_on).split(',')[0] }}</span>
                </div>
                <div class="fw-semibold text-muted">Registered</div>
              </div>
              <!--end::Stats-->
            </div>
            <!--end::Patient Info-->
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
                <a :href="`mailto:${contact?.info?.email || contact?.email}`" class="text-gray-600 text-hover-primary">
                  {{ contact?.info?.email || contact?.email || 'No email' }}
                </a>
              </div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Phone</div>
              <div class="text-gray-600">
                <a :href="`tel:${contact?.info?.phone || contact?.phone}`" class="text-gray-600 text-hover-primary">
                  {{ contact?.info?.phone || contact?.phone || 'No phone' }}
                </a>
              </div>
              <!--end::Details item-->              
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Date of Birth</div>
              <div class="text-gray-600">{{ formatDate(contact?.date_of_birth || contact?.info?.date_of_birth) }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Nationality</div>
              <div class="text-gray-600">{{ contact?.nationality || contact?.info?.nationality || 'Not specified' }}</div>
              <!--end::Details item-->
              
              <!--begin::Details item-->
              <div class="fw-bold mt-5">Address</div>
              <div class="text-gray-600">
                {{ getFormattedAddress() }}
              </div>
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
            <h3 class="fw-bold m-0">Patient Information</h3>
          </div>
        </div>
        <!--end::Card header-->

        <!--begin::Card body-->
        <div class="card-body pt-2">
          <div class="py-2">
            <!--begin::Patient Details-->
            <div class="fw-bold mt-3">Passport Number</div>
            <div class="text-gray-600">{{ contact?.passport_number || 'Not provided' }}</div>
            
            <div class="fw-bold mt-5">Passport Expiration</div>
            <div class="text-gray-600">{{ formatDate(contact?.passport_expiration_date) }}</div>
            
            <div class="fw-bold mt-5">Special Instructions</div>
            <div class="text-gray-600">{{ contact?.special_instructions || 'None' }}</div>
            
            <div class="fw-bold mt-5">Bed at Origin</div>
            <div class="text-gray-600">{{ contact?.bed_at_origin ? 'Yes' : 'No' }}</div>
            
            <div class="fw-bold mt-5">Bed at Destination</div>
            <div class="text-gray-600">{{ contact?.bed_at_destination ? 'Yes' : 'No' }}</div>
            <!--end::Patient Details-->
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

export default defineComponent({
  name: "contact-details",
  components: {
    ContactOverview,
  },
  setup() {
    const route = useRoute();
    const contact = ref<any>(null);
    const loading = ref(true);
    const error = ref<string | null>(null);
    const contactRoles = ref<Array<{type: string, label: string, color: string, icon: string}>>([]);

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
            // First try as patient ID
            endpoint = `/patients/${contactId}/`;
            try {
              const response = await ApiService.get(endpoint);
              contact.value = { ...response.data, type: contactType };
              return; // Success, exit early
            } catch (patientErr: any) {
              if (patientErr.response?.status === 404) {
                // If patient not found, try to find patient by contact ID
                console.log('Patient not found by ID, trying to find by contact ID...');
                try {
                  const patientsResponse = await ApiService.get('/patients/');
                  const allPatients = patientsResponse.data.results || patientsResponse.data || [];
                  const matchingPatient = allPatients.find((p: any) => p.info?.id === contactId);
                  
                  if (matchingPatient) {
                    contact.value = { ...matchingPatient, type: contactType };
                    // Update URL to use correct patient ID
                    window.history.replaceState({}, '', `/admin/contacts/patients/${matchingPatient.id}`);
                    return;
                  }
                } catch (searchErr) {
                  console.error('Error searching for patient by contact ID:', searchErr);
                }
              }
              throw patientErr; // Re-throw if we can't handle it
            }
            break;
          case 'customers':
            // Customers are just contacts, use contacts endpoint
            endpoint = `/contacts/${contactId}/`;
            break;
          default:
            endpoint = `/contacts/${contactId}/`;
        }
        
        const response = await ApiService.get(endpoint);
        contact.value = { ...response.data, type: contactType };
        
        // After fetching contact, detect roles
        await detectContactRoles();
        
      } catch (err: any) {
        error.value = err.response?.data?.detail || "Failed to fetch contact details";
        console.error("Error fetching contact:", err);
      } finally {
        loading.value = false;
      }
    };

    const detectContactRoles = async () => {
      if (!contact.value) return;
      
      const roles: Array<{type: string, label: string, color: string, icon: string}> = [];
      const contactId = contact.value.id || contact.value.info?.id;
      
      try {
        // Check if contact is a patient
        const patientsResponse = await ApiService.get('/patients/');
        const patients = patientsResponse.data.results || patientsResponse.data || [];
        const isPatientRecord = patients.some((p: any) => p.info?.id === contactId || p.id === contactId);
        
        if (isPatientRecord) {
          roles.push({
            type: 'patient',
            label: 'Patient',
            color: 'danger',
            icon: 'ki-heart-pulse'
          });
        }

        // Check if contact is a passenger
        const passengersResponse = await ApiService.get('/passengers/');
        const passengers = passengersResponse.data.results || passengersResponse.data || [];
        const isPassengerRecord = passengers.some((p: any) => p.info?.id === contactId);
        
        if (isPassengerRecord) {
          roles.push({
            type: 'passenger',
            label: 'Passenger',
            color: 'info',
            icon: 'ki-people'
          });
        }

        // Check if contact is staff
        const staffResponse = await ApiService.get('/staff/');
        const staff = staffResponse.data.results || staffResponse.data || [];
        const isStaffRecord = staff.some((s: any) => s.contact?.id === contactId || s.info?.id === contactId);
        
        if (isStaffRecord) {
          roles.push({
            type: 'staff',
            label: 'Staff',
            color: 'primary',
            icon: 'ki-badge'
          });
        }

        // If no specific roles found, add general contact badge
        if (roles.length === 0) {
          roles.push({
            type: 'contact',
            label: 'Contact',
            color: 'secondary',
            icon: 'ki-profile-circle'
          });
        }

        contactRoles.value = roles;
        
      } catch (error) {
        console.error('Error detecting contact roles:', error);
        // Fallback to general contact badge
        contactRoles.value = [{
          type: 'contact',
          label: 'Contact',
          color: 'secondary',
          icon: 'ki-profile-circle'
        }];
      }
    };

    const getContactInitials = (): string => {
      if (contact.value) {
        // For patients, get name from info object
        const firstName = contact.value.info?.first_name || contact.value.first_name;
        const lastName = contact.value.info?.last_name || contact.value.last_name;
        const email = contact.value.info?.email || contact.value.email;
        
        const first = firstName?.charAt(0) || '';
        const last = lastName?.charAt(0) || '';
        return (first + last).toUpperCase() || email?.charAt(0).toUpperCase() || 'C';
      }
      return 'C';
    };

    const getContactName = (): string => {
      if (contact.value) {
        // For patients, get name from info object
        const firstName = contact.value.info?.first_name || contact.value.first_name;
        const lastName = contact.value.info?.last_name || contact.value.last_name;
        const email = contact.value.info?.email || contact.value.email;
        
        const name = `${firstName || ''} ${lastName || ''}`.trim();
        return name || email || 'Unknown Contact';
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
    
    const getPatientAge = (): string => {
      if (!contact.value?.date_of_birth) return 'Unknown';
      
      const today = new Date();
      const birthDate = new Date(contact.value.date_of_birth);
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      
      return `${age}y`;
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
      
      // For patients, get address from info object  
      const addressData = contact.value.info || contact.value;
      const parts = [
        addressData.address_line1,
        addressData.address_line2,
        addressData.city,
        addressData.state,
        addressData.zip,
        addressData.country
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
      contactRoles,
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
      getPatientAge,
    };
  },
});
</script>