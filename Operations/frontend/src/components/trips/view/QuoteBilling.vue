<template>
  <!--begin::Card-->
  <div class="card card-flush pt-3 mb-5 mb-xl-10">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Quote & Billing</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-primary me-3">
          <KTIcon icon-name="pencil" icon-class="fs-3" />
          Edit Quote
        </button>
        <button class="btn btn-primary">
          <KTIcon icon-name="printer" icon-class="fs-3" />
          Generate Invoice
        </button>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-3">
      <!--begin::Quote Summary-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Quote Summary:</h5>
        <!--end::Title-->

        <!--begin::Quote Card-->
        <div class="card card-bordered mb-6">
          <div class="card-body p-6">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <div class="fs-4 fw-bold text-gray-900 mb-2">{{ getQuoteNumber() }}</div>
                <div class="fs-6 text-gray-700">
                  <span class="fw-semibold">Status:</span>
                  <span :class="`badge badge-light-${getQuoteStatusColor()} ms-2`">
                    {{ getQuoteStatus() }}
                  </span>
                </div>
              </div>
              <div class="text-end">
                <div class="fs-2 fw-bold text-gray-900">{{ getTotalAmount() }}</div>
                <div class="fs-7 text-gray-600">Total Cost</div>
              </div>
            </div>
          </div>
        </div>
        <!--end::Quote Card-->
      </div>
      <!--end::Quote Summary-->

      <!--begin::Cost Breakdown-->
      <div class="mb-10">
        <!--begin::Title-->
        <h5 class="mb-4">Cost Breakdown:</h5>
        <!--end::Title-->

        <!--begin::Cost Table-->
        <div class="table-responsive">
          <table class="table table-row-bordered table-row-gray-100 align-middle gs-0 gy-4">
            <!--begin::Table head-->
            <thead>
              <tr class="fw-bold text-muted bg-light">
                <th class="ps-4 min-w-200px rounded-start">Service</th>
                <th class="min-w-70px text-end">Qty</th>
                <th class="min-w-100px text-end">Rate</th>
                <th class="min-w-100px text-end rounded-end">Amount</th>
              </tr>
            </thead>
            <!--end::Table head-->

            <!--begin::Table body-->
            <tbody>
              <!--begin::Row-->
              <tr>
                <td class="ps-4">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="airplane" icon-class="fs-3 text-primary me-3" />
                    <div>
                      <div class="fw-bold text-gray-900 fs-6">Aircraft Charter</div>
                      <div class="text-gray-600 fs-7">{{ getAircraftModel() }} hourly rate</div>
                    </div>
                  </div>
                </td>
                <td class="text-end fw-bold text-gray-900 fs-6">{{ getFlightHours() }}</td>
                <td class="text-end fw-bold text-gray-900 fs-6">${{ getHourlyRate() }}/hr</td>
                <td class="text-end fw-bold text-gray-900 fs-6">${{ getAircraftCost() }}</td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="ps-4">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="medical-08" icon-class="fs-3 text-success me-3" />
                    <div>
                      <div class="fw-bold text-gray-900 fs-6">Medical Services</div>
                      <div class="text-gray-600 fs-7">Flight nurse and paramedic</div>
                    </div>
                  </div>
                </td>
                <td class="text-end fw-bold text-gray-900 fs-6">1</td>
                <td class="text-end fw-bold text-gray-900 fs-6">$2,500</td>
                <td class="text-end fw-bold text-gray-900 fs-6">$2,500</td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="ps-4">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="oil" icon-class="fs-3 text-warning me-3" />
                    <div>
                      <div class="fw-bold text-gray-900 fs-6">Fuel Surcharge</div>
                      <div class="text-gray-600 fs-7">{{ getFuelQuantity() }} lbs @ ${{ getFuelRate() }}/lb</div>
                    </div>
                  </div>
                </td>
                <td class="text-end fw-bold text-gray-900 fs-6">{{ getFuelQuantity() }}</td>
                <td class="text-end fw-bold text-gray-900 fs-6">${{ getFuelRate() }}/lb</td>
                <td class="text-end fw-bold text-gray-900 fs-6">${{ getFuelCost() }}</td>
              </tr>
              <!--end::Row-->

              <!--begin::Row-->
              <tr>
                <td class="ps-4">
                  <div class="d-flex align-items-center">
                    <KTIcon icon-name="geolocation" icon-class="fs-3 text-info me-3" />
                    <div>
                      <div class="fw-bold text-gray-900 fs-6">Ground Services</div>
                      <div class="text-gray-600 fs-7">Handling, ramp fees, permits</div>
                    </div>
                  </div>
                </td>
                <td class="text-end fw-bold text-gray-900 fs-6">1</td>
                <td class="text-end fw-bold text-gray-900 fs-6">$850</td>
                <td class="text-end fw-bold text-gray-900 fs-6">$850</td>
              </tr>
              <!--end::Row-->
            </tbody>
            <!--end::Table body-->
          </table>
        </div>
        <!--end::Cost Table-->

        <!--begin::Total Section-->
        <div class="d-flex flex-stack bg-light-primary rounded p-6 mt-6">
          <div class="fs-6 fw-bold text-gray-700">
            <div class="d-flex justify-content-between mb-2">
              <span>Subtotal:</span>
              <span>${{ getSubtotal() }}</span>
            </div>
            <div class="d-flex justify-content-between mb-2">
              <span>Tax (8.5%):</span>
              <span>${{ getTaxAmount() }}</span>
            </div>
            <div class="separator separator-dashed my-3"></div>
            <div class="d-flex justify-content-between">
              <span class="fs-4 fw-bold text-gray-900">Total:</span>
              <span class="fs-4 fw-bold text-gray-900">{{ getTotalAmount() }}</span>
            </div>
          </div>
        </div>
        <!--end::Total Section-->
      </div>
      <!--end::Cost Breakdown-->

      <!--begin::Payment Status-->
      <div class="mb-0">
        <!--begin::Title-->
        <h5 class="mb-4">Payment Status:</h5>
        <!--end::Title-->

        <!--begin::Payment Info-->
        <div class="row g-6">
          <!--begin::Payment Status Card-->
          <div class="col-md-6">
            <div class="card card-bordered">
              <div class="card-body p-6">
                <div class="d-flex align-items-center mb-4">
                  <KTIcon icon-name="credit-card" icon-class="fs-1 text-success me-3" />
                  <div>
                    <div class="fw-bold fs-6 text-gray-900">Payment Method</div>
                    <div class="text-gray-700 fs-7">Insurance + Card</div>
                  </div>
                </div>
                <div class="fs-7 text-gray-700">
                  <div class="mb-2">
                    <span class="fw-semibold">Insurance Coverage:</span> 80%
                  </div>
                  <div class="mb-2">
                    <span class="fw-semibold">Patient Responsibility:</span> 20%
                  </div>
                  <div>
                    <span class="fw-semibold">Payment Status:</span>
                    <span class="badge badge-light-warning ms-2">Pending</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Payment Status Card-->

          <!--begin::Insurance Info Card-->
          <div class="col-md-6">
            <div class="card card-bordered">
              <div class="card-body p-6">
                <div class="d-flex align-items-center mb-4">
                  <KTIcon icon-name="shield-check" icon-class="fs-1 text-primary me-3" />
                  <div>
                    <div class="fw-bold fs-6 text-gray-900">Insurance Provider</div>
                    <div class="text-gray-700 fs-7">Blue Cross Blue Shield</div>
                  </div>
                </div>
                <div class="fs-7 text-gray-700">
                  <div class="mb-2">
                    <span class="fw-semibold">Policy Number:</span> BCBS-12345-6789
                  </div>
                  <div class="mb-2">
                    <span class="fw-semibold">Authorization:</span> AUTH-2024-5678
                  </div>
                  <div>
                    <span class="fw-semibold">Coverage Amount:</span> ${{ getInsuranceCoverage() }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Insurance Info Card-->
        </div>
        <!--end::Payment Info-->
      </div>
      <!--end::Payment Status-->
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Card-->
</template>

<script setup lang="ts">
interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();

const getQuoteNumber = (): string => {
  return props.trip?.quote?.quote_number || `Q-${props.trip?.trip_number || '2025-001'}`;
};

const getQuoteStatus = (): string => {
  return props.trip?.quote?.status || 'Approved';
};

const getQuoteStatusColor = (): string => {
  const status = getQuoteStatus().toLowerCase();
  switch (status) {
    case 'approved': return 'success';
    case 'pending': return 'warning';
    case 'rejected': return 'danger';
    default: return 'secondary';
  }
};

const getAircraftModel = (): string => {
  return props.trip?.aircraft?.model || 'Cessna Citation CJ4';
};

const getFlightHours = (): string => {
  const hours = props.trip?.flight_time ? (props.trip.flight_time / 60).toFixed(1) : '2.5';
  return `${hours} hrs`;
};

const getHourlyRate = (): string => {
  return props.trip?.quote?.hourly_rate || '4,500';
};

const getAircraftCost = (): string => {
  const hours = props.trip?.flight_time ? props.trip.flight_time / 60 : 2.5;
  const rate = parseInt(getHourlyRate().replace(',', ''));
  return (hours * rate).toLocaleString();
};

const getFuelQuantity = (): string => {
  return props.trip?.fuel_required || '1,200';
};

const getFuelRate = (): string => {
  return '6.25';
};

const getFuelCost = (): string => {
  const quantity = parseInt(getFuelQuantity().replace(',', ''));
  const rate = parseFloat(getFuelRate());
  return (quantity * rate).toLocaleString();
};

const getSubtotal = (): string => {
  const aircraft = parseInt(getAircraftCost().replace(',', ''));
  const medical = 2500;
  const fuel = parseInt(getFuelCost().replace(',', ''));
  const ground = 850;
  return (aircraft + medical + fuel + ground).toLocaleString();
};

const getTaxAmount = (): string => {
  const subtotal = parseInt(getSubtotal().replace(',', ''));
  return (subtotal * 0.085).toLocaleString();
};

const getTotalAmount = (): string => {
  const subtotal = parseInt(getSubtotal().replace(',', ''));
  const tax = parseInt(getTaxAmount().replace(',', ''));
  return `$${(subtotal + tax).toLocaleString()}`;
};

const getInsuranceCoverage = (): string => {
  const total = parseInt(getSubtotal().replace(',', '')) + parseInt(getTaxAmount().replace(',', ''));
  return (total * 0.8).toLocaleString();
};
</script>