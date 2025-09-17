<template>
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <!--begin::Title-->
      <h2 class="fw-bold d-flex align-items-center text-gray-900">
        User Information
        <span class="ms-1" data-bs-toggle="tooltip" title="Enter the basic information for the new user">
          <i class="ki-duotone ki-information-5 text-gray-500 fs-6">
            <span class="path1"></span>
            <span class="path2"></span>
            <span class="path3"></span>
          </i>
        </span>
      </h2>
      <!--end::Title-->

      <!--begin::Notice-->
      <div class="text-muted fw-semibold fs-6">
        The user will receive an email with a link to set their password and complete their profile.
      </div>
      <!--end::Notice-->
    </div>
    <!--end::Heading-->

    <!--begin::Input group-->
    <div class="row mb-10">
      <!--begin::Col-->
      <div class="col-md-6 fv-row">
        <!--begin::Label-->
        <label class="required fs-6 fw-semibold mb-2">First Name</label>
        <!--end::Label-->
        <!--begin::Input-->
        <input
          type="text"
          class="form-control form-control-solid"
          :class="{'is-invalid': errors.first_name}"
          placeholder="Enter first name"
          v-model="localData.first_name"
          @input="validateAndEmit"
        />
        <!--end::Input-->
        <div v-if="errors.first_name" class="invalid-feedback">
          {{ errors.first_name }}
        </div>
      </div>
      <!--end::Col-->

      <!--begin::Col-->
      <div class="col-md-6 fv-row">
        <!--begin::Label-->
        <label class="required fs-6 fw-semibold mb-2">Last Name</label>
        <!--end::Label-->
        <!--begin::Input-->
        <input
          type="text"
          class="form-control form-control-solid"
          :class="{'is-invalid': errors.last_name}"
          placeholder="Enter last name"
          v-model="localData.last_name"
          @input="validateAndEmit"
        />
        <!--end::Input-->
        <div v-if="errors.last_name" class="invalid-feedback">
          {{ errors.last_name }}
        </div>
      </div>
      <!--end::Col-->
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-10 fv-row">
      <!--begin::Label-->
      <label class="required fs-6 fw-semibold mb-2">Email Address</label>
      <!--end::Label-->
      <!--begin::Input-->
      <input
        type="email"
        class="form-control form-control-solid"
        :class="{'is-invalid': errors.email}"
        placeholder="Enter email address"
        v-model="localData.email"
        @input="validateAndEmit"
      />
      <!--end::Input-->
      <div v-if="errors.email" class="invalid-feedback">
        {{ errors.email }}
      </div>
      <div class="form-text">
        This email will be used to send the account activation link.
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-10 fv-row">
      <!--begin::Label-->
      <label class="fs-6 fw-semibold mb-2">
        User Roles
        <span class="ms-1" data-bs-toggle="tooltip" title="Select one or more roles for this user">
          <i class="ki-duotone ki-information-5 text-gray-500 fs-6">
            <span class="path1"></span>
            <span class="path2"></span>
            <span class="path3"></span>
          </i>
        </span>
      </label>
      <!--end::Label-->

      <!--begin::Roles-->
      <div class="d-flex flex-column">
        <div v-if="roles.length === 0" class="text-muted">
          Loading roles...
        </div>
        <div v-else>
          <div v-for="role in roles" :key="role.id" class="form-check form-check-custom form-check-solid mb-3">
            <input
              class="form-check-input"
              type="checkbox"
              :value="role.id"
              :id="`role_${role.id}`"
              v-model="localData.role_ids"
              @change="validateAndEmit"
            />
            <label class="form-check-label fw-semibold text-gray-700 fs-6" :for="`role_${role.id}`">
              {{ role.name }}
              <span v-if="role.description" class="text-muted fs-7 d-block">
                {{ role.description }}
              </span>
            </label>
          </div>
          <div v-if="localData.role_ids.length === 0" class="form-text">
            Select at least one role for the user (optional, can be assigned later).
          </div>
        </div>
      </div>
      <!--end::Roles-->
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-10 fv-row">
      <!--begin::Label-->
      <label class="fs-6 fw-semibold mb-2">Email Options</label>
      <!--end::Label-->

      <!--begin::Options-->
      <div class="form-check form-check-custom form-check-solid">
        <input
          class="form-check-input"
          type="checkbox"
          id="send_activation_email"
          v-model="localData.send_activation_email"
          @change="validateAndEmit"
        />
        <label class="form-check-label fw-semibold text-gray-700 fs-6" for="send_activation_email">
          Send activation email to user
          <span class="text-muted fs-7 d-block">
            The user will receive an email with instructions to set their password and complete their profile.
          </span>
        </label>
      </div>
      <!--end::Options-->
    </div>
    <!--end::Input group-->
  </div>
</template>

<script setup lang="ts">
import { reactive, watch, onMounted } from 'vue';

interface UserData {
  first_name: string;
  last_name: string;
  email: string;
  role_ids: string[];
  send_activation_email: boolean;
}

interface Role {
  id: string;
  name: string;
  description?: string;
}

interface Props {
  modelValue: UserData;
  roles: Role[];
  errors: Record<string, string>;
}

interface Emits {
  (e: 'update:modelValue', value: UserData): void;
  (e: 'step-validated', isValid: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Local copy of the data for two-way binding
const localData = reactive<UserData>({
  first_name: '',
  last_name: '',
  email: '',
  role_ids: [],
  send_activation_email: true
});

// Sync local data with prop on mount and prop changes
const syncFromProps = () => {
  localData.first_name = props.modelValue.first_name;
  localData.last_name = props.modelValue.last_name;
  localData.email = props.modelValue.email;
  localData.role_ids = [...props.modelValue.role_ids];
  localData.send_activation_email = props.modelValue.send_activation_email;
};

// Validate the current step
const validateStep = (): boolean => {
  const requiredFields = ['first_name', 'last_name', 'email'];

  for (const field of requiredFields) {
    if (!localData[field as keyof UserData] || String(localData[field as keyof UserData]).trim() === '') {
      return false;
    }
  }

  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(localData.email)) {
    return false;
  }

  return true;
};

// Emit updates and validation
const validateAndEmit = () => {
  console.log('BasicInfoStep - validateAndEmit called with localData:', localData);

  // Emit the updated data
  emit('update:modelValue', { ...localData });

  // Emit validation status
  const isValid = validateStep();
  console.log('BasicInfoStep - validation result:', isValid);
  emit('step-validated', isValid);
};

// Watch for external prop changes
watch(() => props.modelValue, syncFromProps, { deep: true });

// Initial sync and validation
onMounted(() => {
  syncFromProps();
  validateAndEmit();
});
</script>