<template>
  <!--begin::Modal - Create staff role-->
  <div
    class="modal fade"
    id="kt_modal_create_staff_role"
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
          <h2>Create New Staff Role</h2>
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
          <form id="kt_modal_create_staff_role_form" class="form">
            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Role Code</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter role code (e.g., PIC, SIC, RN)"
                name="code"
                v-model="formData.code"
                :disabled="isSubmitting"
                @input="formatCode"
              />
              <div class="form-text">
                Short code for the role. Will be automatically converted to uppercase.
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Input group-->
            <div class="fv-row mb-8">
              <label class="required fs-6 fw-semibold mb-2">Role Name</label>
              <input
                type="text"
                class="form-control form-control-solid"
                placeholder="Enter full role name (e.g., Pilot in Command)"
                name="name"
                v-model="formData.name"
                :disabled="isSubmitting"
              />
              <div class="form-text">
                Full descriptive name for the role.
              </div>
            </div>
            <!--end::Input group-->

            <!--begin::Role Preview-->
            <div v-if="formData.code || formData.name" class="card bg-light-info mb-8">
              <div class="card-body">
                <h5 class="card-title">Role Preview</h5>
                <div class="d-flex align-items-center">
                  <span 
                    :class="`badge badge-light-${getRoleColor(formData.code)} fs-6 fw-bold me-3`"
                  >
                    {{ formData.code || 'CODE' }}
                  </span>
                  <div>
                    <div class="fw-bold">{{ formData.name || 'Role Name' }}</div>
                    <div class="text-muted fs-7">{{ formData.code || 'CODE' }}</div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Role Preview-->

            <!--begin::Common Role Templates-->
            <div class="separator separator-content my-10">
              <span class="w-250px fw-bold text-gray-600">Or Use Common Template</span>
            </div>

            <div class="mb-8">
              <label class="fs-6 fw-semibold mb-4">Common Staff Roles</label>
              <div class="row g-3">
                <div v-for="template in roleTemplates" :key="template.code" class="col-md-6">
                  <div 
                    class="card card-flush border border-gray-300 cursor-pointer" 
                    :class="{ 'border-primary bg-light-primary': isTemplateSelected(template) }"
                    @click="applyTemplate(template)"
                  >
                    <div class="card-body p-4">
                      <div class="d-flex align-items-center">
                        <span 
                          :class="`badge badge-light-${getRoleColor(template.code)} me-3`"
                        >
                          {{ template.code }}
                        </span>
                        <div>
                          <div class="fw-bold">{{ template.name }}</div>
                          <div class="text-muted fs-7">{{ template.description }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!--end::Common Role Templates-->
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
            :disabled="isSubmitting || !formData.code || !formData.name"
          >
            <span v-if="!isSubmitting" class="indicator-label">Create Role</span>
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
  <!--end::Modal - Create staff role-->
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { hideModal } from "@/core/helpers/modal";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);

// Form data
const formData = reactive({
  code: '',
  name: '',
});

// Emit event to parent
const emit = defineEmits(['roleCreated']);

// Common role templates
const roleTemplates = ref([
  {
    code: 'PIC',
    name: 'Pilot in Command',
    description: 'Primary flight crew'
  },
  {
    code: 'SIC',
    name: 'Second in Command',
    description: 'Co-pilot'
  },
  {
    code: 'RN',
    name: 'Registered Nurse',
    description: 'Medical crew'
  },
  {
    code: 'PARAMEDIC',
    name: 'Paramedic',
    description: 'Emergency medical technician'
  },
  {
    code: 'MD',
    name: 'Medical Doctor',
    description: 'Physician'
  },
  {
    code: 'RT',
    name: 'Respiratory Therapist',
    description: 'Respiratory specialist'
  },
  {
    code: 'EMT',
    name: 'Emergency Medical Technician',
    description: 'Basic emergency medical care'
  },
  {
    code: 'DISPATCHER',
    name: 'Dispatcher',
    description: 'Operations coordinator'
  },
]);

const getRoleColor = (roleCode: string): string => {
  const colors: Record<string, string> = {
    PIC: 'primary',
    SIC: 'info',
    RN: 'success',
    PARAMEDIC: 'warning',
    MD: 'danger',
    RT: 'secondary',
    EMT: 'dark',
    DISPATCHER: 'info',
  };
  return colors[roleCode] || 'secondary';
};

const formatCode = () => {
  // Convert to uppercase and remove spaces/special characters
  formData.code = formData.code.toUpperCase().replace(/[^A-Z0-9]/g, '');
};

const isTemplateSelected = (template: any): boolean => {
  return formData.code === template.code && formData.name === template.name;
};

const applyTemplate = (template: any) => {
  formData.code = template.code;
  formData.name = template.name;
};

const handleSubmit = async (e: Event) => {
  e.preventDefault();
  
  // Basic validation
  if (!formData.code || !formData.name) {
    Swal.fire({
      title: "Validation Error",
      text: "Please fill in both role code and name",
      icon: "warning",
      confirmButtonText: "OK"
    });
    return;
  }

  isSubmitting.value = true;
  
  try {
    const roleData = {
      code: formData.code.trim(),
      name: formData.name.trim(),
    };

    console.log('Creating staff role with data:', roleData);
    const response = await ApiService.post('/staff-roles/', roleData);
    console.log('Staff role created successfully:', response.data);
    
    Swal.fire({
      title: "Success!",
      text: "Staff role created successfully!",
      icon: "success",
      confirmButtonText: "OK"
    }).then(() => {
      hideModal(modalRef.value);
      emit('roleCreated', response.data);
      resetForm();
    });
  } catch (error: any) {
    console.error('Error creating staff role:', error);
    
    let errorMessage = "Failed to create staff role. Please try again.";
    
    if (error.response?.data) {
      if (error.response.data.code && error.response.data.code.includes('already exists')) {
        errorMessage = `A role with the code "${formData.code}" already exists. Please use a different code.`;
      } else if (typeof error.response.data === 'object') {
        const errors = Object.values(error.response.data).flat();
        errorMessage = errors.join('. ');
      } else {
        errorMessage = error.response.data.detail || error.response.data.message || errorMessage;
      }
    }
    
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
  formData.code = '';
  formData.name = '';
};
</script>