<template>
  <!--begin::Wrapper-->
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <h2 class="fw-bold text-gray-900">Review & Create Trip</h2>
      <div class="text-muted fw-semibold fs-6">
        Review all trip details before creating the trip.
      </div>
    </div>
    <!--end::Heading-->

    <!--begin::Review Sections-->
    <div class="d-flex flex-column gap-7 gap-lg-10">
      <!--begin::Trip Info-->
      <div class="card card-flush py-4">
        <div class="card-header">
          <div class="card-title">
            <h2>Trip Information</h2>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="table-responsive">
            <table class="table align-middle table-row-bordered mb-0 fs-6 gy-5">
              <tbody class="fw-semibold text-gray-600">
                <tr>
                  <td class="text-muted min-w-125px w-125px">Trip Number:</td>
                  <td class="fs-5 text-gray-900 fw-bold">JM-2025-001</td>
                </tr>
                <tr>
                  <td class="text-muted">Type:</td>
                  <td>Medical Transport</td>
                </tr>
                <tr>
                  <td class="text-muted">Priority:</td>
                  <td><span class="badge badge-light-warning">Urgent</span></td>
                </tr>
                <tr>
                  <td class="text-muted">Service Level:</td>
                  <td>Advanced Life Support</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!--end::Trip Info-->

      <!--begin::Patient Info-->
      <div class="card card-flush py-4">
        <div class="card-header">
          <div class="card-title">
            <h2>Patient Information</h2>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="table-responsive">
            <table class="table align-middle table-row-bordered mb-0 fs-6 gy-5">
              <tbody class="fw-semibold text-gray-600">
                <tr>
                  <td class="text-muted min-w-125px w-125px">Patient:</td>
                  <td class="fs-5 text-gray-900 fw-bold">John Doe</td>
                </tr>
                <tr>
                  <td class="text-muted">DOB:</td>
                  <td>January 15, 1980 (45 years old)</td>
                </tr>
                <tr>
                  <td class="text-muted">Condition:</td>
                  <td>Cardiac emergency requiring immediate transport</td>
                </tr>
                <tr>
                  <td class="text-muted">Attending Physician:</td>
                  <td>Dr. Sarah Williams</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!--end::Patient Info-->

      <!--begin::Flight Details-->
      <div class="card card-flush py-4">
        <div class="card-header">
          <div class="card-title">
            <h2>Flight Details</h2>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="table-responsive">
            <table class="table align-middle table-row-bordered mb-0 fs-6 gy-5">
              <tbody class="fw-semibold text-gray-600">
                <tr>
                  <td class="text-muted min-w-125px w-125px">Route:</td>
                  <td class="fs-5 text-gray-900 fw-bold">KORD → KLAX</td>
                </tr>
                <tr>
                  <td class="text-muted">Departure:</td>
                  <td>December 20, 2024 at 2:30 PM</td>
                </tr>
                <tr>
                  <td class="text-muted">Estimated Flight Time:</td>
                  <td>4h 15m</td>
                </tr>
                <tr>
                  <td class="text-muted">Distance:</td>
                  <td>1,745 nautical miles</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!--end::Flight Details-->

      <!--begin::Aircraft & Crew-->
      <div class="card card-flush py-4">
        <div class="card-header">
          <div class="card-title">
            <h2>Aircraft & Crew</h2>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="table-responsive">
            <table class="table align-middle table-row-bordered mb-0 fs-6 gy-5">
              <tbody class="fw-semibold text-gray-600">
                <tr>
                  <td class="text-muted min-w-125px w-125px">Aircraft:</td>
                  <td class="fs-5 text-gray-900 fw-bold">N123JM - Cessna Citation CJ4</td>
                </tr>
                <tr>
                  <td class="text-muted">Pilot in Command:</td>
                  <td>Capt. John Smith</td>
                </tr>
                <tr>
                  <td class="text-muted">Flight Nurse:</td>
                  <td>RN Jennifer White (CEN, CFRN)</td>
                </tr>
                <tr>
                  <td class="text-muted">Flight Paramedic:</td>
                  <td>EMT-P James Miller (FP-C)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <!--end::Aircraft & Crew-->
    </div>
    <!--end::Review Sections-->

    <!--begin::Confirmation-->
    <div class="d-flex flex-stack">
      <div class="me-5">
        <label class="fs-6 fw-semibold form-label">Ready to create this trip?</label>
        <div class="fs-7 fw-semibold text-muted">
          Once created, this trip will be added to the active trips list and crew will be notified.
        </div>
      </div>
      <label class="form-check form-switch form-check-custom form-check-solid">
        <input class="form-check-input" name="send_notifications" type="checkbox" value="1" checked="checked" />
        <span class="form-check-label fw-semibold text-muted">
          Send notifications to crew
        </span>
      </label>
    </div>
    <!--end::Confirmation-->
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
// Step 5 - Review & Create
</script>