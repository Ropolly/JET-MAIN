<template>
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-12">
      <!--begin::Title-->
      <h2 class="fw-bold text-gray-900">Confirm User Creation</h2>
      <!--end::Title-->

      <!--begin::Notice-->
      <div class="text-muted fw-semibold fs-6">
        Please review the user information below and confirm to create the account.
      </div>
      <!--end::Notice-->
    </div>
    <!--end::Heading-->

    <!--begin::Review-->
    <div class="mb-0">
      <!--begin::User Information-->
      <div class="d-flex flex-column mb-8">
        <div class="fs-6 fw-bold text-gray-700 mb-4">User Information</div>

        <div class="d-flex flex-stack mb-3">
          <div class="fw-semibold pe-10 text-gray-600 fs-7">Name:</div>
          <div class="text-end fw-bold fs-6 text-gray-800">
            {{ userData.first_name }} {{ userData.last_name }}
          </div>
        </div>

        <div class="d-flex flex-stack mb-3">
          <div class="fw-semibold pe-10 text-gray-600 fs-7">Email:</div>
          <div class="text-end fw-bold fs-6 text-gray-800">
            {{ userData.email }}
          </div>
        </div>

        <div class="d-flex flex-stack mb-3">
          <div class="fw-semibold pe-10 text-gray-600 fs-7">Roles:</div>
          <div class="text-end fw-bold fs-6 text-gray-800">
            <span v-if="selectedRoleNames.length > 0">
              {{ selectedRoleNames.join(', ') }}
            </span>
            <span v-else class="text-muted">No roles assigned</span>
          </div>
        </div>

        <div class="d-flex flex-stack">
          <div class="fw-semibold pe-10 text-gray-600 fs-7">Send Email:</div>
          <div class="text-end fw-bold fs-6 text-gray-800">
            <span v-if="userData.send_activation_email" class="badge badge-light-success">
              <i class="ki-duotone ki-check fs-7"></i>
              Yes
            </span>
            <span v-else class="badge badge-light-warning">
              <i class="ki-duotone ki-cross fs-7"></i>
              No
            </span>
          </div>
        </div>
      </div>
      <!--end::User Information-->

      <!--begin::Separator-->
      <div class="separator separator-dashed mb-8"></div>
      <!--end::Separator-->

      <!--begin::Process Info-->
      <div class="d-flex flex-column">
        <div class="fs-6 fw-bold text-gray-700 mb-4">What happens next?</div>

        <div class="d-flex align-items-start mb-6">
          <span class="bullet bullet-vertical h-40px bg-success"></span>
          <div class="ms-5">
            <div class="fs-6 fw-semibold text-gray-700">User account created</div>
            <div class="fs-7 text-muted">
              A new user account will be created with the information provided above.
            </div>
          </div>
        </div>

        <div v-if="userData.send_activation_email" class="d-flex align-items-start mb-6">
          <span class="bullet bullet-vertical h-40px bg-primary"></span>
          <div class="ms-5">
            <div class="fs-6 fw-semibold text-gray-700">Activation email sent</div>
            <div class="fs-7 text-muted">
              An email with activation instructions will be sent to {{ userData.email }}.
            </div>
          </div>
        </div>

        <div class="d-flex align-items-start mb-6">
          <span class="bullet bullet-vertical h-40px bg-info"></span>
          <div class="ms-5">
            <div class="fs-6 fw-semibold text-gray-700">User sets password</div>
            <div class="fs-7 text-muted">
              {{ userData.send_activation_email
                ? 'The user will click the email link and set their password.'
                : 'You will need to provide the user with login instructions.' }}
            </div>
          </div>
        </div>

        <div class="d-flex align-items-start">
          <span class="bullet bullet-vertical h-40px bg-warning"></span>
          <div class="ms-5">
            <div class="fs-6 fw-semibold text-gray-700">Profile completion</div>
            <div class="fs-7 text-muted">
              The user will be prompted to add their phone number and complete their profile.
            </div>
          </div>
        </div>
      </div>
      <!--end::Process Info-->

      <!--begin::Notice-->
      <div v-if="!userData.send_activation_email" class="notice d-flex bg-light-warning rounded border-warning border border-dashed p-6 mt-8">
        <i class="ki-duotone ki-information-5 fs-2tx text-warning me-4">
          <span class="path1"></span>
          <span class="path2"></span>
          <span class="path3"></span>
        </i>
        <div class="d-flex flex-stack flex-grow-1">
          <div class="fw-semibold">
            <h4 class="text-gray-900 fw-bold">Email Not Enabled</h4>
            <div class="fs-6 text-gray-700">
              Since you've chosen not to send an activation email, you'll need to manually provide
              the user with their login credentials and instructions to access the system.
            </div>
          </div>
        </div>
      </div>
      <!--end::Notice-->
    </div>
    <!--end::Review-->
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';

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
  userData: UserData;
  roles: Role[];
  isSubmitting: boolean;
}

interface Emits {
  (e: 'step-validated', isValid: boolean): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// Computed property to get selected role names
const selectedRoleNames = computed(() => {
  return props.userData.role_ids
    .map(roleId => {
      const role = props.roles.find(r => r.id === roleId);
      return role ? role.name : null;
    })
    .filter(Boolean) as string[];
});

// This step is always valid since it's just confirmation
onMounted(() => {
  emit('step-validated', true);
});
</script>