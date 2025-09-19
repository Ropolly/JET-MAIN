<template>
  <!--begin::Modal - Create staff-->
  <div
    class="modal fade"
    id="kt_modal_create_staff"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-lg">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Add New Staff Member</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Modal body-->
        <div class="modal-body scroll-y mx-5 my-7">
          <!--begin::Form-->
          <form id="kt_modal_create_staff_form" class="form">
            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Contact</label>
              <select 
                name="contact" 
                class="form-select form-select-solid" 
                v-model="formData.contact_id"
                :disabled="isSubmitting"
              >
                <option value="">Select contact to make staff member...</option>
                <option 
                  v-for="contact in availableContacts" 
                  :key="contact.id" 
                  :value="contact.id"
                >
                  {{ getContactDisplayName(contact) }}
                </option>
              </select>
              <div class="form-text">Only contacts that are not already staff members are shown.</div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Status</label>
              <div class="form-check form-switch">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="formData.active"
                  id="staffActiveSwitch"
                  :disabled="isSubmitting"
                >
                <label class="form-check-label fw-semibold text-gray-700" for="staffActiveSwitch">
                  {{ formData.active ? 'Active' : 'Inactive' }}
                </label>
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Initial Roles</label>
              <select 
                name="roles" 
                class="form-select form-select-solid" 
                v-model="formData.initial_roles" 
                multiple
                :disabled="isSubmitting"
              >
                <option 
                  v-for="role in staffRoles" 
                  :key="role.id" 
                  :value="role.id"
                >
                  {{ role.name }} ({{ role.code }})
                </option>
              </select>
              <div class="form-text">Hold Ctrl/Cmd to select multiple roles. You can also assign roles later.</div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="fs-6 fw-semibold mb-2">Notes</label>
              <textarea
                class="form-control form-control-solid"
                rows="3"
                name="notes"
                placeholder="Additional notes about this staff member..."
                v-model="formData.notes"
                :disabled="isSubmitting"
              ></textarea>
            </div>
            <!--end::Input group-->

            <!--begin::Contact Creation Section-->
            <div v-if="showCreateContact" class="separator separator-content my-10">
              <span class="w-250px fw-bold text-gray-600">Or Create New Contact</span>
            </div>

            <div v-if="showCreateContact" class="mb-8">
              <!--begin::Toggle-->
              <div class="form-check form-switch mb-5">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  v-model="createNewContact"
                  id="createContactSwitch"
                  :disabled="isSubmitting"
                >
                <label class="form-check-label fw-semibold text-gray-700" for="createContactSwitch">
                  Create new contact and make them a staff member
                </label>
              </div>

              <div v-if="createNewContact">
                <!--begin::Name fields-->
                <div class="row g-9 mb-8">
                  <div class="col-md-6 fv-row">
                    <label class="fs-6 fw-semibold mb-2">First Name</label>
                    <input
                      type="text"
                      class="form-control form-control-solid"
                      placeholder="First name"
                      name="first_name"
                      v-model="newContact.first_name"
                      :disabled="isSubmitting"
                    />
                  </div>
                  <div class="col-md-6 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Last Name</label>
                    <input
                      type="text"
                      class="form-control form-control-solid"
                      placeholder="Last name"
                      name="last_name"
                      v-model="newContact.last_name"
                      :disabled="isSubmitting"
                    />
                  </div>
                </div>

                <!--begin::Contact fields-->
                <div class="row g-9 mb-8">
                  <div class="col-md-6 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Email</label>
                    <input
                      type="email"
                      class="form-control form-control-solid"
                      placeholder="Email address"
                      name="email"
                      v-model="newContact.email"
                      :disabled="isSubmitting"
                    />
                  </div>
                  <div class="col-md-6 fv-row">
                    <label class="fs-6 fw-semibold mb-2">Phone</label>
                    <input
                      type="text"
                      class="form-control form-control-solid"
                      placeholder="Phone number"
                      name="phone"
                      v-model="newContact.phone"
                      :disabled="isSubmitting"
                    />
                  </div>
                </div>

                <!--begin::Business name-->
                <div class="fv-row mb-8">
                  <label class="fs-6 fw-semibold mb-2">Business Name</label>
                  <input
                    type="text"
                    class="form-control form-control-solid"
                    placeholder="Business name (optional)"
                    name="business_name"
                    v-model="newContact.business_name"
                    :disabled="isSubmitting"
                  />
                  <div class="form-text">Leave blank if this is an individual contact</div>
                </div>
              </div>
            </div>
            <!--end::Contact Creation Section-->
          </form>
          <!--end::Form-->
        </div>
        <!--end::Modal body-->

        <!--begin::Modal footer-->
        <div class="modal-footer flex-center">
          <!--begin::Button-->
          <button
            type="reset"
            class="btn btn-light me-3"
            data-bs-dismiss="modal"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <!--end::Button-->

          <!--begin::Button-->
          <button
            type="submit"
            class="btn btn-primary"
            @click="handleSubmit"
            :disabled="isSubmitting"
          >
            <span v-if="!isSubmitting" class="indicator-label">
              {{ createNewContact ? 'Create Contact & Staff' : 'Add Staff Member' }}
            </span>
            <span v-else class="indicator-progress">
              Please wait...
              <span
                class="spinner-border spinner-border-sm align-middle ms-2"
              ></span>
            </span>
          </button>
          <!--end::Button-->
        </div>
        <!--end::Modal footer-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create staff-->
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from "vue";
import { hideModal } from "@/core/helpers/modal";
import { Modal } from "bootstrap";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Form data
const formData = reactive({
  contact_id: '',
  active: true,
  notes: '',
  initial_roles: [] as string[],
});

// New contact data
const createNewContact = ref(false);
const showCreateContact = ref(true);
const newContact = reactive({
  first_name: '',
  last_name: '',
  business_name: '',
  email: '',
  phone: '',
});

// Dropdown data
const contacts = ref<any[]>([]);
const staffRoles = ref<any[]>([]);

// Emit event to parent
const emit = defineEmits(['staffCreated']);

// Computed
const availableContacts = computed(() => {
  return contacts.value.filter(contact => !contact.is_staff);
});

// Fetch dropdown data
const fetchDropdownData = async () => {
  try {
    // Fetch all contacts
    const contactsResponse = await ApiService.get('/contacts/?page_size=100');
    contacts.value = contactsResponse.data.results || contactsResponse.data || [];
    
    // Check which contacts are already staff
    const staffResponse = await ApiService.get('/staff/?page_size=100');
    const existingStaff = staffResponse.data.results || staffResponse.data || [];
    const staffContactIds = existingStaff.map((staff: any) => staff.contact_id);
    
    // Mark contacts that are already staff
    contacts.value = contacts.value.map(contact => ({
      ...contact,
      is_staff: staffContactIds.includes(contact.id)
    }));

    console.log('Available contacts for staff:', availableContacts.value.length);
  } catch (error) {
    console.error('Error fetching contacts:', error);
  }
  
  try {
    // Fetch staff roles
    const rolesResponse = await ApiService.get('/staff-roles/');
    staffRoles.value = rolesResponse.data.results || rolesResponse.data || [];
    console.log('Loaded staff roles:', staffRoles.value.length);
  } catch (error) {
    console.error('Error fetching staff roles:', error);
  }
};

onMounted(() => {
  fetchDropdownData();
});

const getContactDisplayName = (contact: any): string => {
  if (!contact) return 'Unknown Contact';
  
  const firstName = contact.first_name || '';
  const lastName = contact.last_name || '';
  const businessName = contact.business_name || '';
  const email = contact.email || '';
  
  if (businessName) {
    return `${businessName}${email ? ` (${email})` : ''}`;
  }
  
  const fullName = `${firstName} ${lastName}`.trim();
  if (fullName) {
    return `${fullName}${email ? ` (${email})` : ''}`;
  }
  
  return email || 'Unknown Contact';
};

const createContact = async (): Promise<string> => {
  // Validate required fields
  if (!newContact.first_name && !newContact.last_name && !newContact.business_name) {
    throw new Error('Either first/last name or business name is required for new contact');
  }

  const contactData = {
    first_name: newContact.first_name,
    last_name: newContact.last_name,
    business_name: newContact.business_name,
    email: newContact.email,
    phone: newContact.phone,
    status: 'active'
  };

  console.log('Creating new contact:', contactData);
  const response = await ApiService.post('/contacts/', contactData);
  console.log('Contact created:', response.data);
  
  return response.data.id;
};

const createStaffRoleMemberships = async (staffId: string) => {
  if (formData.initial_roles.length === 0) return;

  const today = new Date().toISOString().split('T')[0];

  for (const roleId of formData.initial_roles) {
    try {
      const membershipData = {
        staff_id: staffId,
        role_id: roleId,
        start_on: today
      };

      console.log('Creating role membership:', membershipData);
      await ApiService.post('/staff-role-memberships/', membershipData);
    } catch (error) {
      console.error('Error creating role membership:', error);
      // Don't fail the whole operation if role assignment fails
    }
  }
};

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!createNewContact.value && !formData.contact_id) {
    Swal.fire({
      title: "Validation Error",
      text: "Please select a contact or choose to create a new one",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;
  
  try {
    let contactId = formData.contact_id;

    // Create new contact if needed
    if (createNewContact.value) {
      contactId = await createContact();
    }

    // Create staff member
    const staffData = {
      contact_id: contactId,
      active: formData.active,
      notes: formData.notes
    };

    console.log('Creating staff with data:', staffData);
    const staffResponse = await ApiService.post('/staff/', staffData);
    console.log('Staff created successfully:', staffResponse.data);

    // Create initial role memberships
    await createStaffRoleMemberships(staffResponse.data.id);
    
    const successMessage = createNewContact.value
      ? "Contact and staff member created successfully!"
      : "Staff member created successfully!";

    Swal.fire({
      title: "Success!",
      text: successMessage,
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      // Close modal using Bootstrap Modal API
      const modalElement = modalRef.value;
      if (modalElement) {
        try {
          const modal = Modal.getInstance(modalElement);
          if (modal) {
            modal.hide();
          } else {
            // Fallback: manually close modal
            modalElement.classList.remove('show');
            modalElement.style.display = 'none';
            modalElement.setAttribute('aria-hidden', 'true');
            modalElement.removeAttribute('aria-modal');
            document.body.classList.remove('modal-open');
            document.body.style.paddingRight = '';
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) backdrop.remove();
          }
        } catch (error) {
          console.error('Error closing modal:', error);
          // Manual fallback
          modalElement.classList.remove('show');
          modalElement.style.display = 'none';
          modalElement.setAttribute('aria-hidden', 'true');
          modalElement.removeAttribute('aria-modal');
          document.body.classList.remove('modal-open');
          document.body.style.paddingRight = '';
          const backdrop = document.querySelector('.modal-backdrop');
          if (backdrop) backdrop.remove();
        }
      }
      
      emit('staffCreated', staffResponse.data);
      resetForm();
    });
  } catch (error: any) {
    console.error('Error creating staff:', error);
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        "Failed to create staff member. Please try again.";
    
    Swal.fire({
      title: "Error!",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};

const resetForm = () => {
  formData.contact_id = '';
  formData.active = true;
  formData.notes = '';
  formData.initial_roles = [];
  
  createNewContact.value = false;
  newContact.first_name = '';
  newContact.last_name = '';
  newContact.business_name = '';
  newContact.email = '';
  newContact.phone = '';
};
</script>