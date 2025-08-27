<template>
  <div>
    <!--begin::Contact Information-->
    <div class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="required fs-6 fw-semibold mb-2">Full Name</label>
        <input
          v-model="passengerData.contact_name"
          type="text"
          class="form-control form-control-solid"
          placeholder="Enter passenger name..."
        />
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Email Address</label>
        <input
          v-model="passengerData.contact_email"
          type="email"
          class="form-control form-control-solid"
          placeholder="passenger@example.com"
        />
      </div>
    </div>
    <!--end::Contact Information-->

    <!--begin::Phone-->
    <div class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Phone Number</label>
        <input
          v-model="passengerData.contact_phone"
          type="tel"
          class="form-control form-control-solid"
          placeholder="(555) 123-4567"
        />
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Emergency Contact</label>
        <input
          v-model="passengerData.emergency_contact"
          type="text"
          class="form-control form-control-solid"
          placeholder="Emergency contact name & number"
        />
      </div>
    </div>
    <!--end::Phone-->

    <!--begin::Travel Documents-->
    <div class="separator separator-dashed my-5"></div>
    <h6 class="fw-bold text-gray-700 mb-4">Travel Documents (Optional)</h6>
    
    <div class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
        <input
          v-model="passengerData.date_of_birth"
          type="date"
          class="form-control form-control-solid"
        />
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Nationality</label>
        <input
          v-model="passengerData.nationality"
          type="text"
          class="form-control form-control-solid"
          placeholder="e.g., US, Canadian, etc."
        />
      </div>
    </div>

    <div class="row g-9 mb-5">
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Passport Number</label>
        <input
          v-model="passengerData.passport_number"
          type="text"
          class="form-control form-control-solid"
          placeholder="Passport number"
        />
      </div>
      <div class="col-md-6 fv-row">
        <label class="fs-6 fw-semibold mb-2">Passport Expiration</label>
        <input
          v-model="passengerData.passport_expiration_date"
          type="date"
          class="form-control form-control-solid"
        />
      </div>
    </div>
    <!--end::Travel Documents-->

    <!--begin::Special Notes-->
    <div class="fv-row">
      <label class="fs-6 fw-semibold mb-2">Special Requirements</label>
      <textarea
        v-model="passengerData.special_notes"
        class="form-control form-control-solid"
        rows="2"
        placeholder="Any special needs, dietary restrictions, mobility requirements, etc..."
      ></textarea>
    </div>
    <!--end::Special Notes-->

    <!--begin::Create Contact Option-->
    <div class="mt-5 p-4 bg-light rounded">
      <div class="form-check">
        <input
          v-model="passengerData.create_as_contact"
          class="form-check-input"
          type="checkbox"
          :id="`create_contact_${passengerData.id}`"
        />
        <label class="form-check-label fs-7" :for="`create_contact_${passengerData.id}`">
          <strong>Create as Contact:</strong> Save this passenger information as a reusable contact record in the system for future trips.
        </label>
      </div>
    </div>
    <!--end::Create Contact Option-->
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const passengerData = props.modelValue;

// Ensure all required fields exist on the passenger object
if (!passengerData.emergency_contact) passengerData.emergency_contact = '';
if (!passengerData.date_of_birth) passengerData.date_of_birth = '';
if (!passengerData.nationality) passengerData.nationality = '';
if (!passengerData.passport_number) passengerData.passport_number = '';
if (!passengerData.passport_expiration_date) passengerData.passport_expiration_date = '';
if (!passengerData.special_notes) passengerData.special_notes = '';
if (passengerData.create_as_contact === undefined) passengerData.create_as_contact = true;
</script>