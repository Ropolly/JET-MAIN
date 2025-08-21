<template>
  <!--begin::Wrapper-->
  <div class="w-100">
    <!--begin::Heading-->
    <div class="pb-10 pb-lg-15">
      <h2 class="fw-bold text-gray-900">Flight Details</h2>
      <div class="text-muted fw-semibold fs-6">
        Configure departure, arrival, and timing information for the trip.
      </div>
    </div>
    <!--end::Heading-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <div class="col-md-6 fv-row">
        <label class="required form-label">Departure Airport</label>
        <select name="departure_airport" class="form-select form-select-solid">
          <option value="">Select departure airport...</option>
          <option value="KORD">Chicago O'Hare (KORD)</option>
          <option value="KMDW">Chicago Midway (KMDW)</option>
          <option value="KLAX">Los Angeles (KLAX)</option>
          <option value="KJFK">JFK New York (KJFK)</option>
          <option value="KDEN">Denver (KDEN)</option>
        </select>
      </div>
      <div class="col-md-6 fv-row">
        <label class="required form-label">Arrival Airport</label>
        <select name="arrival_airport" class="form-select form-select-solid">
          <option value="">Select arrival airport...</option>
          <option value="KORD">Chicago O'Hare (KORD)</option>
          <option value="KMDW">Chicago Midway (KMDW)</option>
          <option value="KLAX">Los Angeles (KLAX)</option>
          <option value="KJFK">JFK New York (KJFK)</option>
          <option value="KDEN">Denver (KDEN)</option>
        </select>
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <div class="col-md-6 fv-row">
        <label class="required form-label">Departure Date</label>
        <input name="departure_date" type="date" class="form-control form-control-solid" />
      </div>
      <div class="col-md-6 fv-row">
        <label class="required form-label">Departure Time</label>
        <input name="departure_time" type="time" class="form-control form-control-solid" />
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <div class="col-md-6 fv-row">
        <label class="form-label">Return Date (if applicable)</label>
        <input name="return_date" type="date" class="form-control form-control-solid" />
      </div>
      <div class="col-md-6 fv-row">
        <label class="form-label">Return Time (if applicable)</label>
        <input name="return_time" type="time" class="form-control form-control-solid" />
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-8 fv-row">
      <div class="form-check form-switch form-check-custom form-check-solid">
        <input class="form-check-input" type="checkbox" name="is_round_trip" id="is_round_trip" />
        <label class="form-check-label fw-semibold text-gray-400 ms-3" for="is_round_trip">
          Round Trip
        </label>
      </div>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="mb-8 fv-row">
      <label class="form-label">Flight Notes</label>
      <textarea name="flight_notes" class="form-control form-control-solid" rows="3" placeholder="Any special requirements, weather considerations, or additional notes"></textarea>
    </div>
    <!--end::Input group-->

    <!--begin::Input group-->
    <div class="row g-9 mb-8">
      <div class="col-md-4 fv-row">
        <label class="form-label">Estimated Flight Time</label>
        <input name="estimated_flight_time" class="form-control form-control-solid" placeholder="2h 30m" />
      </div>
      <div class="col-md-4 fv-row">
        <label class="form-label">Distance (nm)</label>
        <input name="distance" type="number" class="form-control form-control-solid" placeholder="250" />
      </div>
      <div class="col-md-4 fv-row">
        <label class="form-label">Fuel Required (lbs)</label>
        <input name="fuel_required" type="number" class="form-control form-control-solid" placeholder="1200" />
      </div>
    </div>
    <!--end::Input group-->
  </div>
  <!--end::Wrapper-->
</template>

<script setup lang="ts">
// Step 3 - Flight Details
</script>