<template>
  <!--begin::Wrapper-->
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <!--begin::Title-->
      <h2 class="fw-bold text-gray-900">Trip Type</h2>
      <!--end::Title-->

      <!--begin::Notice-->
      <div class="text-muted fw-semibold fs-6">
        Select the type of trip you want to create and provide basic information.
      </div>
      <!--end::Notice-->
    </div>
    <!--end::Heading-->

    <!--begin::Input group-->
    <div class="mb-10 fv-row">
      <!--begin::Label-->
      <label class="form-label mb-3">Trip Type</label>
      <!--end::Label-->

      <!--begin::Input-->
      <div class="row">
        <!--begin::Col-->
        <div class="col-lg-6">
          <!--begin::Option-->
          <input
            type="radio"
            class="btn-check"
            name="trip_type"
            value="medical"
            checked="checked"
            id="kt_create_trip_type_medical"
          />
          <label
            class="btn btn-outline btn-outline-dashed btn-active-light-primary p-7 d-flex align-items-center mb-10"
            for="kt_create_trip_type_medical"
          >
            <!--begin::Icon-->
            <i class="ki-duotone ki-medical-08 fs-1 text-primary me-4">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
            <!--end::Icon-->

            <!--begin::Info-->
            <div class="d-flex flex-column align-items-start">
              <div class="fw-bold fs-5 text-gray-900 text-start">
                Medical Transport
              </div>
              <div class="fs-7 fw-semibold text-muted text-start">
                Emergency or scheduled medical transport
              </div>
            </div>
            <!--end::Info-->
          </label>
          <!--end::Option-->
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-lg-6">
          <!--begin::Option-->
          <input
            type="radio"
            class="btn-check"
            name="trip_type"
            value="charter"
            id="kt_create_trip_type_charter"
          />
          <label
            class="btn btn-outline btn-outline-dashed btn-active-light-primary p-7 d-flex align-items-center mb-10"
            for="kt_create_trip_type_charter"
          >
            <!--begin::Icon-->
            <i class="ki-duotone ki-airplane fs-1 text-primary me-4">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
            <!--end::Icon-->

            <!--begin::Info-->
            <div class="d-flex flex-column align-items-start">
              <div class="fw-bold fs-5 text-gray-900 text-start">
                Charter Flight
              </div>
              <div class="fs-7 fw-semibold text-muted text-start">
                Private charter for passengers or cargo
              </div>
            </div>
            <!--end::Info-->
          </label>
          <!--end::Option-->
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-lg-6">
          <!--begin::Option-->
          <input
            type="radio"
            class="btn-check"
            name="trip_type"
            value="part91"
            id="kt_create_trip_type_part91"
          />
          <label
            class="btn btn-outline btn-outline-dashed btn-active-light-primary p-7 d-flex align-items-center mb-10"
            for="kt_create_trip_type_part91"
          >
            <!--begin::Icon-->
            <i class="ki-duotone ki-briefcase fs-1 text-primary me-4">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
            <!--end::Icon-->

            <!--begin::Info-->
            <div class="d-flex flex-column align-items-start">
              <div class="fw-bold fs-5 text-gray-900 text-start">
                Part 91 Flight
              </div>
              <div class="fs-7 fw-semibold text-muted text-start">
                Private operation under Part 91 regulations
              </div>
            </div>
            <!--end::Info-->
          </label>
          <!--end::Option-->
        </div>
        <!--end::Col-->

        <!--begin::Col-->
        <div class="col-lg-6">
          <!--begin::Option-->
          <input
            type="radio"
            class="btn-check"
            name="trip_type"
            value="maintenance"
            id="kt_create_trip_type_maintenance"
          />
          <label
            class="btn btn-outline btn-outline-dashed btn-active-light-primary p-7 d-flex align-items-center mb-10"
            for="kt_create_trip_type_maintenance"
          >
            <!--begin::Icon-->
            <i class="ki-duotone ki-wrench fs-1 text-primary me-4">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
            <!--end::Icon-->

            <!--begin::Info-->
            <div class="d-flex flex-column align-items-start">
              <div class="fw-bold fs-5 text-gray-900 text-start">
                Maintenance Flight
              </div>
              <div class="fs-7 fw-semibold text-muted text-start">
                Aircraft maintenance or positioning flight
              </div>
            </div>
            <!--end::Info-->
          </label>
          <!--end::Option-->
        </div>
        <!--end::Col-->
      </div>
      <!--end::Input-->
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-10 fv-row">
      <!--begin::Label-->
      <label class="required form-label">Trip Number</label>
      <!--end::Label-->

      <!--begin::Input-->
      <input
        name="trip_number"
        class="form-control form-control-lg form-control-solid"
        value=""
        placeholder="Enter trip number (e.g., JM-2025-001)"
      />
      <!--end::Input-->
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <!--begin::Col-->
      <div class="col-md-6 fv-row">
        <label class="required form-label">Priority Level</label>
        <select name="priority" class="form-select form-select-solid">
          <option value="">Select priority...</option>
          <option value="routine">Routine</option>
          <option value="urgent">Urgent</option>
          <option value="emergency">Emergency</option>
          <option value="critical">Critical</option>
        </select>
      </div>
      <!--end::Col-->

      <!--begin::Col-->
      <div class="col-md-6 fv-row">
        <label class="required form-label">Service Level</label>
        <select name="service_level" class="form-select form-select-solid">
          <option value="">Select service level...</option>
          <option value="basic">Basic Transport</option>
          <option value="advanced">Advanced Life Support</option>
          <option value="critical_care">Critical Care</option>
          <option value="specialty">Specialty Care</option>
        </select>
      </div>
      <!--end::Col-->
    </div>
    <!--end::Input group-->
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
// Step 1 - Trip Type Selection
</script>