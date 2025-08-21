<template>
  <!--begin::Wrapper-->
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <h2 class="fw-bold text-gray-900">Patient Information</h2>
      <div class="text-muted fw-semibold fs-6">
        Enter patient details and medical requirements for this trip.
      </div>
    </div>
    <!--end::Heading-->

    <!--begin::Input group-->
    <div class="mb-8 fv-row">
      <label class="form-label">Existing Patient</label>
      <select name="patient_id" class="form-select form-select-solid">
        <option value="">Select existing patient or add new...</option>
        <option value="new">+ Add New Patient</option>
        <option value="1">John Doe (DOB: 1980-01-15)</option>
        <option value="2">Jane Smith (DOB: 1975-03-20)</option>
      </select>
    </div>
    <!--end::Input group-->

    <div id="new-patient-form" style="display: none;">
      <!--begin::Input group-->
      <div class="row g-9 mb-8">
        <div class="col-md-6 fv-row">
          <label class="required form-label">First Name</label>
          <input name="patient_first_name" class="form-control form-control-solid" />
        </div>
        <div class="col-md-6 fv-row">
          <label class="required form-label">Last Name</label>
          <input name="patient_last_name" class="form-control form-control-solid" />
        </div>
      </div>
      <!--end::Input group-->

      <!--begin::Input group-->
      <div class="row g-9 mb-8">
        <div class="col-md-4 fv-row">
          <label class="required form-label">Date of Birth</label>
          <input name="patient_dob" type="date" class="form-control form-control-solid" />
        </div>
        <div class="col-md-4 fv-row">
          <label class="required form-label">Gender</label>
          <select name="patient_gender" class="form-select form-select-solid">
            <option value="">Select...</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="col-md-4 fv-row">
          <label class="form-label">Weight (lbs)</label>
          <input name="patient_weight" type="number" class="form-control form-control-solid" />
        </div>
      </div>
      <!--end::Input group-->
    </div>

    <!--begin::Input group-->
    <div class="mb-8 fv-row">
      <label class="form-label">Medical Condition</label>
      <textarea name="medical_condition" class="form-control form-control-solid" rows="3" placeholder="Brief description of patient's condition and transport requirements"></textarea>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <div class="col-md-6 fv-row">
        <label class="form-label">Attending Physician</label>
        <input name="attending_physician" class="form-control form-control-solid" placeholder="Dr. Name" />
      </div>
      <div class="col-md-6 fv-row">
        <label class="form-label">Medical Equipment Needed</label>
        <select name="medical_equipment" class="form-select form-select-solid" multiple>
          <option value="ventilator">Ventilator</option>
          <option value="iv_pump">IV Pump</option>
          <option value="monitor">Cardiac Monitor</option>
          <option value="oxygen">Oxygen Tank</option>
          <option value="stretcher">Stretcher</option>
        </select>
      </div>
    </div>
    <!--end::Input group-->
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
// Step 2 - Patient Information
</script>