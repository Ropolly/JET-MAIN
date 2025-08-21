<template>
  <!--begin::Wrapper-->
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <h2 class="fw-bold text-gray-900">Aircraft & Crew</h2>
      <div class="text-muted fw-semibold fs-6">
        Select aircraft and assign crew members for this trip.
      </div>
    </div>
    <!--end::Heading-->

    <!--begin::Input group-->
    <div class="mb-8 fv-row">
      <label class="required form-label">Aircraft</label>
      <select name="aircraft_id" class="form-select form-select-solid">
        <option value="">Select aircraft...</option>
        <option value="1">N123JM - Cessna Citation CJ4 (Available)</option>
        <option value="2">N456JM - King Air 350 (Available)</option>
        <option value="3">N789JM - Beechcraft Premier (Maintenance)</option>
        <option value="4">N101JM - Pilatus PC-12 (Available)</option>
      </select>
    </div>
    <!--end::Input group-->

    <!--begin::Aircraft Details-->
    <div id="aircraft-details" class="mb-8" style="display: none;">
      <div class="border border-gray-300 border-dashed rounded p-6 bg-light-info">
        <div class="row g-6">
          <div class="col-md-3">
            <div class="fw-bold text-gray-800">Max Passengers:</div>
            <div class="text-muted">8 passengers</div>
          </div>
          <div class="col-md-3">
            <div class="fw-bold text-gray-800">Range:</div>
            <div class="text-muted">2,165 nm</div>
          </div>
          <div class="col-md-3">
            <div class="fw-bold text-gray-800">Medical Config:</div>
            <div class="text-muted">Full stretcher</div>
          </div>
          <div class="col-md-3">
            <div class="fw-bold text-gray-800">Last Inspection:</div>
            <div class="text-muted">2024-12-15</div>
          </div>
        </div>
      </div>
    </div>
    <!--end::Aircraft Details-->

    <!--begin::Crew Section-->
    <div class="mb-8">
      <h3 class="fw-bold text-gray-900 mb-5">Flight Crew</h3>
      
      <!--begin::Pilot in Command-->
      <div class="row g-9 mb-6">
        <div class="col-md-6 fv-row">
          <label class="required form-label">Pilot in Command (PIC)</label>
          <select name="pic_id" class="form-select form-select-solid">
            <option value="">Select PIC...</option>
            <option value="1">Capt. John Smith (ATP, Type Rated)</option>
            <option value="2">Capt. Sarah Johnson (ATP, Type Rated)</option>
            <option value="3">Capt. Mike Wilson (ATP, Type Rated)</option>
          </select>
        </div>
        <div class="col-md-6 fv-row">
          <label class="form-label">Second in Command (SIC)</label>
          <select name="sic_id" class="form-select form-select-solid">
            <option value="">Select SIC (if required)...</option>
            <option value="4">FO David Brown (Commercial)</option>
            <option value="5">FO Lisa Davis (Commercial)</option>
            <option value="6">FO Robert Taylor (ATP)</option>
          </select>
        </div>
      </div>
      <!--end::Pilot in Command-->
    </div>
    <!--end::Crew Section-->

    <!--begin::Medical Crew Section-->
    <div class="mb-8">
      <h3 class="fw-bold text-gray-900 mb-5">Medical Crew</h3>
      
      <!--begin::Medical Staff-->
      <div class="row g-9 mb-6">
        <div class="col-md-6 fv-row">
          <label class="form-label">Flight Nurse</label>
          <select name="nurse_id" class="form-select form-select-solid">
            <option value="">Select flight nurse...</option>
            <option value="1">RN Jennifer White (CEN, CFRN)</option>
            <option value="2">RN Michael Green (CCRN, CFRN)</option>
            <option value="3">RN Amanda Clark (CEN, FP-C)</option>
          </select>
        </div>
        <div class="col-md-6 fv-row">
          <label class="form-label">Flight Paramedic</label>
          <select name="paramedic_id" class="form-select form-select-solid">
            <option value="">Select paramedic...</option>
            <option value="1">EMT-P James Miller (FP-C)</option>
            <option value="2">EMT-P Karen Anderson (CCP-C)</option>
            <option value="3">EMT-P Steven Wright (FP-C)</option>
          </select>
        </div>
      </div>
      <!--end::Medical Staff-->

      <!--begin::Additional Medical-->
      <div class="row g-9 mb-6">
        <div class="col-md-6 fv-row">
          <label class="form-label">Physician (if required)</label>
          <select name="physician_id" class="form-select form-select-solid">
            <option value="">No physician required...</option>
            <option value="1">Dr. Emily Rodriguez (Emergency Medicine)</option>
            <option value="2">Dr. Thomas Lee (Critical Care)</option>
            <option value="3">Dr. Rachel Kim (Pediatrics)</option>
          </select>
        </div>
        <div class="col-md-6 fv-row">
          <label class="form-label">Respiratory Therapist</label>
          <select name="rt_id" class="form-select form-select-solid">
            <option value="">No RT required...</option>
            <option value="1">RT Paul Johnson (RRT, CRT)</option>
            <option value="2">RT Maria Santos (RRT, RPFT)</option>
          </select>
        </div>
      </div>
      <!--end::Additional Medical-->
    </div>
    <!--end::Medical Crew Section-->

    <!--begin::Crew Notes-->
    <div class="mb-8 fv-row">
      <label class="form-label">Crew Notes</label>
      <textarea name="crew_notes" class="form-control form-control-solid" rows="3" placeholder="Special crew requirements, certifications needed, or scheduling notes"></textarea>
    </div>
    <!--end::Crew Notes-->
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
// Step 4 - Aircraft & Crew
</script>