<template>
  <!--begin::Settings Card-->
  <div class="card card-flush">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Trip Settings</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button
          v-if="hasUnsavedChanges"
          class="btn btn-primary btn-sm me-3"
          @click="saveSettings"
          :disabled="isSaving"
        >
          <span v-if="!isSaving">Save Changes</span>
          <span v-else>
            <span class="spinner-border spinner-border-sm me-2"></span>
            Saving...
          </span>
        </button>
        <button
          v-if="hasUnsavedChanges"
          class="btn btn-light btn-sm"
          @click="resetSettings"
        >
          Reset
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0">
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <div v-if="!loading" class="row g-6">
        <!--begin::Trip Information Section-->
        <div class="col-12">
          <div class="card border border-dashed border-gray-300">
            <div class="card-header border-0">
              <h3 class="card-title fw-bold text-gray-900">
                <KTIcon icon-name="information" icon-class="fs-3 text-primary me-2" />
                Trip Information
              </h3>
            </div>
            <div class="card-body pt-0">
              <div class="row g-5">
                <!--begin::Trip Number-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Trip Number</label>
                  <input
                    type="text"
                    class="form-control form-control-solid"
                    v-model="settings.trip_number"
                    placeholder="Enter trip number"
                  />
                </div>
                <!--end::Trip Number-->

                <!--begin::Trip Type-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Trip Type</label>
                  <select class="form-select form-select-solid" v-model="settings.type">
                    <option value="medical">Medical</option>
                    <option value="charter">Charter</option>
                    <option value="part_91">Part 91</option>
                    <option value="maintenance">Maintenance</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <!--end::Trip Type-->

                <!--begin::Status-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Status</label>
                  <select class="form-select form-select-solid" v-model="settings.status">
                    <option value="pending">Pending</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="active">Active</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
                <!--end::Status-->

                <!--begin::Priority-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Priority</label>
                  <select class="form-select form-select-solid" v-model="settings.priority">
                    <option value="low">Low</option>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
                <!--end::Priority-->

                <!--begin::Notes-->
                <div class="col-12">
                  <label class="form-label fw-semibold">Trip Notes</label>
                  <textarea
                    class="form-control form-control-solid"
                    rows="4"
                    v-model="settings.notes"
                    placeholder="Enter any additional notes or instructions for this trip"
                  ></textarea>
                </div>
                <!--end::Notes-->
              </div>
            </div>
          </div>
        </div>
        <!--end::Trip Information Section-->

        <!--begin::Timing Configuration Section-->
        <div class="col-12">
          <div class="card border border-dashed border-gray-300">
            <div class="card-header border-0">
              <h3 class="card-title fw-bold text-gray-900">
                <KTIcon icon-name="time" icon-class="fs-3 text-warning me-2" />
                Timing Configuration
              </h3>
            </div>
            <div class="card-body pt-0">
              <div class="row g-5">
                <!--begin::Pre-flight Duty Time-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Pre-flight Duty Time</label>
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control form-control-solid"
                      v-model="settings.pre_flight_duty_time"
                      placeholder="60"
                      min="0"
                      step="15"
                    />
                    <span class="input-group-text">minutes</span>
                  </div>
                  <div class="form-text">Time required before first departure</div>
                </div>
                <!--end::Pre-flight Duty Time-->

                <!--begin::Post-flight Duty Time-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Post-flight Duty Time</label>
                  <div class="input-group">
                    <input
                      type="number"
                      class="form-control form-control-solid"
                      v-model="settings.post_flight_duty_time"
                      placeholder="30"
                      min="0"
                      step="15"
                    />
                    <span class="input-group-text">minutes</span>
                  </div>
                  <div class="form-text">Time required after final arrival</div>
                </div>
                <!--end::Post-flight Duty Time-->

                <!--begin::Estimated Departure Time-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Estimated Departure Time</label>
                  <input
                    type="datetime-local"
                    class="form-control form-control-solid"
                    v-model="settings.estimated_departure_time"
                  />
                  <div class="form-text">Initial departure time for trip planning</div>
                </div>
                <!--end::Estimated Departure Time-->
              </div>
            </div>
          </div>
        </div>
        <!--end::Timing Configuration Section-->

        <!--begin::Notification Settings Section-->
        <div class="col-12">
          <div class="card border border-dashed border-gray-300">
            <div class="card-header border-0">
              <h3 class="card-title fw-bold text-gray-900">
                <KTIcon icon-name="notification-status" icon-class="fs-3 text-info me-2" />
                Notification Settings
              </h3>
            </div>
            <div class="card-body pt-0">
              <div class="row g-5">
                <!--begin::Email Notifications-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="symbol symbol-40px me-4">
                        <span class="symbol-label bg-light-primary">
                          <KTIcon icon-name="sms" icon-class="fs-2 text-primary" />
                        </span>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">Email Notifications</div>
                        <div class="fs-7 text-muted">Send updates via email</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.notifications.email_enabled"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::Email Notifications-->

                <!--begin::SMS Notifications-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="symbol symbol-40px me-4">
                        <span class="symbol-label bg-light-success">
                          <KTIcon icon-name="phone" icon-class="fs-2 text-success" />
                        </span>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">SMS Notifications</div>
                        <div class="fs-7 text-muted">Send updates via text</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.notifications.sms_enabled"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::SMS Notifications-->

                <!--begin::Status Change Notifications-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="symbol symbol-40px me-4">
                        <span class="symbol-label bg-light-warning">
                          <KTIcon icon-name="check-circle" icon-class="fs-2 text-warning" />
                        </span>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">Status Changes</div>
                        <div class="fs-7 text-muted">Notify on status updates</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.notifications.status_changes"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::Status Change Notifications-->

                <!--begin::Schedule Updates-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="symbol symbol-40px me-4">
                        <span class="symbol-label bg-light-danger">
                          <KTIcon icon-name="calendar" icon-class="fs-2 text-danger" />
                        </span>
                      </div>
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">Schedule Updates</div>
                        <div class="fs-7 text-muted">Notify on time changes</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.notifications.schedule_updates"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::Schedule Updates-->
              </div>
            </div>
          </div>
        </div>
        <!--end::Notification Settings Section-->

        <!--begin::Access Control Section-->
        <div class="col-12">
          <div class="card border border-dashed border-gray-300">
            <div class="card-header border-0">
              <h3 class="card-title fw-bold text-gray-900">
                <KTIcon icon-name="security-user" icon-class="fs-3 text-success me-2" />
                Access Control
              </h3>
            </div>
            <div class="card-body pt-0">
              <div class="row g-5">
                <!--begin::Visibility-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Visibility</label>
                  <select class="form-select form-select-solid" v-model="settings.visibility">
                    <option value="public">Public - All users can view</option>
                    <option value="private">Private - Restricted access</option>
                    <option value="team">Team - Team members only</option>
                  </select>
                  <div class="form-text">Control who can access this trip</div>
                </div>
                <!--end::Visibility-->

                <!--begin::Patient Privacy-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">Enhanced Patient Privacy</div>
                        <div class="fs-7 text-muted">Additional HIPAA protections</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.enhanced_privacy"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::Patient Privacy-->

                <!--begin::Audit Logging-->
                <div class="col-md-6">
                  <div class="d-flex flex-stack">
                    <div class="d-flex align-items-center">
                      <div class="d-flex flex-column">
                        <div class="fw-semibold fs-6">Enhanced Audit Logging</div>
                        <div class="fs-7 text-muted">Detailed access tracking</div>
                      </div>
                    </div>
                    <div class="d-flex justify-content-end">
                      <div class="form-check form-switch form-check-custom form-check-solid">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          v-model="settings.enhanced_audit"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <!--end::Audit Logging-->
              </div>
            </div>
          </div>
        </div>
        <!--end::Access Control Section-->

        <!--begin::System Information Section-->
        <div class="col-12">
          <div class="card border border-dashed border-gray-300">
            <div class="card-header border-0">
              <h3 class="card-title fw-bold text-gray-900">
                <KTIcon icon-name="information" icon-class="fs-3 text-secondary me-2" />
                System Information
              </h3>
            </div>
            <div class="card-body pt-0">
              <div class="row g-5">
                <!--begin::Created-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold text-muted">Created</label>
                  <div class="fs-6 text-gray-800">
                    {{ formatDateTime(trip?.created_on) }}
                    <span v-if="trip?.created_by" class="text-muted ms-2">
                      by {{ getUserName(trip.created_by) }}
                    </span>
                  </div>
                </div>
                <!--end::Created-->

                <!--begin::Last Modified-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold text-muted">Last Modified</label>
                  <div class="fs-6 text-gray-800">
                    {{ formatDateTime(trip?.modified_on) }}
                    <span v-if="trip?.modified_by" class="text-muted ms-2">
                      by {{ getUserName(trip.modified_by) }}
                    </span>
                  </div>
                </div>
                <!--end::Last Modified-->

                <!--begin::Trip ID-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold text-muted">Trip ID</label>
                  <div class="fs-6 text-gray-600 font-monospace">{{ trip?.id }}</div>
                </div>
                <!--end::Trip ID-->

                <!--begin::Version-->
                <div class="col-md-6">
                  <label class="form-label fw-semibold text-muted">Version</label>
                  <div class="fs-6 text-gray-800">{{ trip?.version || '1.0' }}</div>
                </div>
                <!--end::Version-->
              </div>
            </div>
          </div>
        </div>
        <!--end::System Information Section-->
      </div>
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Settings Card-->
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits(['tripUpdated']);

const settings = ref<any>({
  trip_number: '',
  type: 'medical',
  status: 'pending',
  priority: 'normal',
  notes: '',
  pre_flight_duty_time: 60,
  post_flight_duty_time: 30,
  estimated_departure_time: '',
  visibility: 'team',
  enhanced_privacy: false,
  enhanced_audit: false,
  notifications: {
    email_enabled: true,
    sms_enabled: false,
    status_changes: true,
    schedule_updates: true
  }
});

const originalSettings = ref<any>({});
const isSaving = ref(false);

// Computed properties
const hasUnsavedChanges = computed(() => {
  return JSON.stringify(settings.value) !== JSON.stringify(originalSettings.value);
});

// Initialize settings from trip data
const initializeSettings = () => {
  if (!props.trip) return;

  const tripSettings = {
    trip_number: props.trip.trip_number || '',
    type: props.trip.type || 'medical',
    status: props.trip.status || 'pending',
    priority: props.trip.priority || 'normal',
    notes: props.trip.notes || '',
    pre_flight_duty_time: props.trip.pre_flight_duty_time || 60,
    post_flight_duty_time: props.trip.post_flight_duty_time || 30,
    estimated_departure_time: props.trip.estimated_departure_time
      ? formatDateTimeForInput(props.trip.estimated_departure_time)
      : '',
    visibility: props.trip.visibility || 'team',
    enhanced_privacy: props.trip.enhanced_privacy || false,
    enhanced_audit: props.trip.enhanced_audit || false,
    notifications: {
      email_enabled: props.trip.notifications?.email_enabled ?? true,
      sms_enabled: props.trip.notifications?.sms_enabled ?? false,
      status_changes: props.trip.notifications?.status_changes ?? true,
      schedule_updates: props.trip.notifications?.schedule_updates ?? true
    }
  };

  settings.value = { ...tripSettings };
  originalSettings.value = { ...tripSettings };
};

// Save settings
const saveSettings = async () => {
  if (isSaving.value) return;

  isSaving.value = true;

  try {
    const updateData = {
      trip_number: settings.value.trip_number,
      type: settings.value.type,
      status: settings.value.status,
      priority: settings.value.priority,
      notes: settings.value.notes,
      pre_flight_duty_time: settings.value.pre_flight_duty_time,
      post_flight_duty_time: settings.value.post_flight_duty_time,
      estimated_departure_time: settings.value.estimated_departure_time || null,
      visibility: settings.value.visibility,
      enhanced_privacy: settings.value.enhanced_privacy,
      enhanced_audit: settings.value.enhanced_audit,
      notifications: settings.value.notifications
    };

    const response = await ApiService.put(`/trips/${props.trip.id}/`, updateData);

    // Update original settings to reflect saved state
    originalSettings.value = { ...settings.value };

    // Emit event to update parent component
    emit('tripUpdated', response.data);

    Swal.fire({
      title: 'Success!',
      text: 'Trip settings have been saved successfully.',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });

  } catch (error) {
    console.error('Error saving settings:', error);
    Swal.fire({
      title: 'Error',
      text: 'Failed to save trip settings. Please try again.',
      icon: 'error'
    });
  } finally {
    isSaving.value = false;
  }
};

// Reset settings
const resetSettings = () => {
  settings.value = { ...originalSettings.value };
};

// Helper functions
const formatDateTime = (datetime: string): string => {
  if (!datetime) return 'Not set';

  try {
    return new Date(datetime).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (error) {
    return 'Invalid date';
  }
};

const formatDateTimeForInput = (datetime: string): string => {
  if (!datetime) return '';

  try {
    const date = new Date(datetime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day}T${hours}:${minutes}`;
  } catch (error) {
    return '';
  }
};

const getUserName = (user: any): string => {
  if (!user) return 'Unknown';

  const first = user.first_name || '';
  const last = user.last_name || '';

  return `${first} ${last}`.trim() || user.username || user.email || 'Unknown';
};

// Watch for trip changes
watch(() => props.trip, () => {
  if (props.trip && !props.loading) {
    initializeSettings();
  }
}, { immediate: true });

// Initialize on mount
onMounted(() => {
  if (props.trip && !props.loading) {
    initializeSettings();
  }
});
</script>

<style scoped>
.font-monospace {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
</style>