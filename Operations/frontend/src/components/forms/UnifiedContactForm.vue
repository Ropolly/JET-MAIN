<template>
  <!--begin::Unified Contact Creation Form-->
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header">
      <div class="card-title">
        <h2>Create New Contact</h2>
      </div>
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body">
      <!--begin::Form-->
      <form @submit.prevent="handleSubmit" class="form">
        
        <!--begin::Contact Type Selection-->
        <div class="row mb-6">
          <label class="col-lg-4 col-form-label required fw-semibold fs-6">Contact Type</label>
          <div class="col-lg-8">
            <select v-model="selectedType" class="form-select form-select-solid" required>
              <option value="">Select contact type</option>
              <option value="patient">Patient</option>
              <option value="staff">Staff Member</option>
              <option value="passenger">Passenger</option>
              <option value="customer">Customer</option>
            </select>
            <div class="text-muted fs-7 mt-1">
              Choose the type of contact you're creating
            </div>
          </div>
        </div>
        <!--end::Contact Type Selection-->

        <!--begin::Personal Information-->
        <div class="separator separator-dashed my-5"></div>
        <h3 class="mb-5">Personal Information</h3>
        
        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">First Name</label>
          <div class="col-lg-8">
            <input
              v-model="formData.first_name"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter first name"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Last Name</label>
          <div class="col-lg-8">
            <input
              v-model="formData.last_name"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter last name"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Business Name</label>
          <div class="col-lg-8">
            <input
              v-model="formData.business_name"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter business name (if applicable)"
            />
            <div class="text-muted fs-7 mt-1">
              Use business name for companies or organizations
            </div>
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Date of Birth</label>
          <div class="col-lg-8">
            <input
              v-model="formData.date_of_birth"
              type="date"
              class="form-control form-control-solid"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Nationality</label>
          <div class="col-lg-8">
            <input
              v-model="formData.nationality"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter nationality"
            />
          </div>
        </div>
        <!--end::Personal Information-->

        <!--begin::Contact Information-->
        <div class="separator separator-dashed my-5"></div>
        <h3 class="mb-5">Contact Information</h3>
        
        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Email</label>
          <div class="col-lg-8">
            <input
              v-model="formData.email"
              type="email"
              class="form-control form-control-solid"
              placeholder="Enter email address"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Phone</label>
          <div class="col-lg-8">
            <input
              v-model="formData.phone"
              type="tel"
              class="form-control form-control-solid"
              placeholder="Enter phone number"
            />
          </div>
        </div>
        <!--end::Contact Information-->

        <!--begin::Passport Information-->
        <div class="separator separator-dashed my-5"></div>
        <h3 class="mb-5">Passport Information</h3>
        
        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Passport Number</label>
          <div class="col-lg-8">
            <input
              v-model="formData.passport_number"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter passport number"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Passport Expiration</label>
          <div class="col-lg-8">
            <input
              v-model="formData.passport_expiration_date"
              type="date"
              class="form-control form-control-solid"
            />
          </div>
        </div>
        <!--end::Passport Information-->

        <!--begin::Address Information-->
        <div class="separator separator-dashed my-5"></div>
        <h3 class="mb-5">Address Information</h3>
        
        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Address Line 1</label>
          <div class="col-lg-8">
            <input
              v-model="formData.address_line1"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter street address"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Address Line 2</label>
          <div class="col-lg-8">
            <input
              v-model="formData.address_line2"
              type="text"
              class="form-control form-control-solid"
              placeholder="Apartment, suite, etc. (optional)"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">City</label>
          <div class="col-lg-8">
            <input
              v-model="formData.city"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter city"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">State/Province</label>
          <div class="col-lg-8">
            <input
              v-model="formData.state"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter state or province"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">ZIP/Postal Code</label>
          <div class="col-lg-8">
            <input
              v-model="formData.zip"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter ZIP or postal code"
            />
          </div>
        </div>

        <div class="row mb-6">
          <label class="col-lg-4 col-form-label fw-semibold fs-6">Country</label>
          <div class="col-lg-8">
            <input
              v-model="formData.country"
              type="text"
              class="form-control form-control-solid"
              placeholder="Enter country"
            />
          </div>
        </div>
        <!--end::Address Information-->

        <!--begin::Type-specific fields-->
        <template v-if="selectedType">
          <div class="separator separator-dashed my-5"></div>
          <h3 class="mb-5">{{ getTypeSpecificTitle() }}</h3>
          
          <!--begin::Patient specific-->
          <template v-if="selectedType === 'patient'">
            <div class="row mb-6">
              <label class="col-lg-4 col-form-label fw-semibold fs-6">Special Instructions</label>
              <div class="col-lg-8">
                <textarea
                  v-model="patientData.special_instructions"
                  class="form-control form-control-solid"
                  rows="3"
                  placeholder="Enter any special medical instructions"
                ></textarea>
              </div>
            </div>
            
            <div class="row mb-6">
              <div class="col-lg-4"></div>
              <div class="col-lg-8">
                <div class="form-check form-check-custom form-check-solid">
                  <input
                    v-model="patientData.bed_at_origin"
                    type="checkbox"
                    class="form-check-input"
                    id="bed_at_origin"
                  />
                  <label class="form-check-label fw-semibold" for="bed_at_origin">
                    Bed required at origin
                  </label>
                </div>
              </div>
            </div>

            <div class="row mb-6">
              <div class="col-lg-4"></div>
              <div class="col-lg-8">
                <div class="form-check form-check-custom form-check-solid">
                  <input
                    v-model="patientData.bed_at_destination"
                    type="checkbox"
                    class="form-check-input"
                    id="bed_at_destination"
                  />
                  <label class="form-check-label fw-semibold" for="bed_at_destination">
                    Bed required at destination
                  </label>
                </div>
              </div>
            </div>
          </template>
          <!--end::Patient specific-->

          <!--begin::Staff specific-->
          <template v-if="selectedType === 'staff'">
            <div class="row mb-6">
              <label class="col-lg-4 col-form-label fw-semibold fs-6">Notes</label>
              <div class="col-lg-8">
                <textarea
                  v-model="staffData.notes"
                  class="form-control form-control-solid"
                  rows="3"
                  placeholder="Enter any notes about this staff member"
                ></textarea>
              </div>
            </div>
            
            <div class="row mb-6">
              <div class="col-lg-4"></div>
              <div class="col-lg-8">
                <div class="form-check form-check-custom form-check-solid">
                  <input
                    v-model="staffData.active"
                    type="checkbox"
                    class="form-check-input"
                    id="staff_active"
                  />
                  <label class="form-check-label fw-semibold" for="staff_active">
                    Active staff member
                  </label>
                </div>
              </div>
            </div>
          </template>
          <!--end::Staff specific-->

          <!--begin::Passenger specific-->
          <template v-if="selectedType === 'passenger'">
            <div class="row mb-6">
              <label class="col-lg-4 col-form-label fw-semibold fs-6">Contact Number</label>
              <div class="col-lg-8">
                <input
                  v-model="passengerData.contact_number"
                  type="tel"
                  class="form-control form-control-solid"
                  placeholder="Emergency contact number"
                />
              </div>
            </div>

            <div class="row mb-6">
              <label class="col-lg-4 col-form-label fw-semibold fs-6">Notes</label>
              <div class="col-lg-8">
                <textarea
                  v-model="passengerData.notes"
                  class="form-control form-control-solid"
                  rows="3"
                  placeholder="Enter any notes about this passenger"
                ></textarea>
              </div>
            </div>
          </template>
          <!--end::Passenger specific-->
        </template>
        <!--end::Type-specific fields-->

        <!--begin::Error Display-->
        <div v-if="hasErrors" class="alert alert-danger">
          <ul class="mb-0">
            <li v-for="error in errors" :key="error">{{ error }}</li>
          </ul>
        </div>
        <!--end::Error Display-->

        <!--begin::Actions-->
        <div class="card-footer d-flex justify-content-end py-6 px-9">
          <button
            type="button"
            @click="handleReset"
            class="btn btn-light btn-active-light-primary me-2"
          >
            Reset
          </button>
          <button
            type="submit"
            :disabled="loading || !selectedType"
            class="btn btn-primary"
          >
            <span v-if="loading" class="indicator-progress">
              Creating...
              <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
            </span>
            <span v-else>Create {{ selectedType || 'Contact' }}</span>
          </button>
        </div>
        <!--end::Actions-->

      </form>
      <!--end::Form-->
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Unified Contact Creation Form-->
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useContactCreation } from '@/composables/useContactCreation';

// Props and emits
interface Props {
  defaultType?: 'patient' | 'staff' | 'passenger' | 'customer';
}

const props = withDefaults(defineProps<Props>(), {
  defaultType: undefined
});

const emit = defineEmits<{
  contactCreated: [contact: any];
  success: [response: any];
  error: [error: string];
}>();

// Use the contact creation composable
const {
  loading,
  errors,
  hasErrors,
  isFormValid,
  formData,
  patientData,
  staffData,
  passengerData,
  clearForm,
  createContact
} = useContactCreation();

// Local state
const selectedType = ref<'patient' | 'staff' | 'passenger' | 'customer' | ''>('');

// Set default type if provided
if (props.defaultType) {
  selectedType.value = props.defaultType;
}

// Computed
const getTypeSpecificTitle = () => {
  const titles: Record<string, string> = {
    'patient': 'Patient Information',
    'staff': 'Staff Information',
    'passenger': 'Passenger Information',
    'customer': 'Customer Information'
  };
  
  return titles[selectedType.value] || 'Additional Information';
};

// Methods
const handleSubmit = async () => {
  if (!selectedType.value) {
    return;
  }
  
  try {
    const response = await createContact(selectedType.value, true);
    
    if (response) {
      emit('contactCreated', response.contact);
      emit('success', response);
      
      // Reset form after successful creation
      selectedType.value = props.defaultType || '';
    }
  } catch (error: any) {
    emit('error', error.message || 'Failed to create contact');
  }
};

const handleReset = () => {
  clearForm();
  selectedType.value = props.defaultType || '';
};
</script>

<style scoped>
.separator {
  margin: 1.5rem 0;
}

.card-footer {
  border-top: 1px dashed var(--bs-gray-300);
  background-color: var(--bs-gray-100);
}
</style>