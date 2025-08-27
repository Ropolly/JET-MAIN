<template>
  <!--begin::Modal - Create contact-->
  <div
    class="modal fade"
    id="kt_modal_create_contact"
    ref="modalRef"
    tabindex="-1"
    aria-hidden="true"
  >
    <!--begin::Modal dialog-->
    <div class="modal-dialog modal-xl">
      <!--begin::Modal content-->
      <div class="modal-content">
        <!--begin::Modal header-->
        <div class="modal-header">
          <!--begin::Title-->
          <h2>Add New Contact - Step {{ currentStep }} of 3</h2>
          <!--end::Title-->

          <!--begin::Close-->
          <div
            class="btn btn-sm btn-icon btn-active-color-primary"
            data-bs-dismiss="modal"
            @click="resetForm"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
          <!--end::Close-->
        </div>
        <!--end::Modal header-->

        <!--begin::Stepper-->
        <div class="stepper stepper-pills stepper-column d-flex flex-column flex-xl-row flex-row-fluid">
          <!--begin::Aside-->
          <div class="d-flex justify-content-center justify-content-xl-start flex-row-auto w-100 w-xl-300px w-xxl-400px me-9">
            <div class="px-6 px-lg-10 px-xxl-15 py-20">
              <!--begin::Nav-->
              <div class="stepper-nav">
                <!--begin::Step 1-->
                <div class="stepper-item" :class="{ current: currentStep === 1, completed: currentStep > 1 }">
                  <div class="stepper-wrapper d-flex align-items-center">
                    <div class="stepper-icon w-40px h-40px">
                      <i class="stepper-check fas fa-check"></i>
                      <span class="stepper-number">1</span>
                    </div>
                    <div class="stepper-label">
                      <h3 class="stepper-title">Basic Information</h3>
                      <div class="stepper-desc">Name and email</div>
                    </div>
                  </div>
                </div>
                <!--end::Step 1-->

                <!--begin::Step 2-->
                <div class="stepper-item" :class="{ current: currentStep === 2, completed: currentStep > 2 }">
                  <div class="stepper-wrapper d-flex align-items-center">
                    <div class="stepper-icon w-40px h-40px">
                      <i class="stepper-check fas fa-check"></i>
                      <span class="stepper-number">2</span>
                    </div>
                    <div class="stepper-label">
                      <h3 class="stepper-title">Phone & Location</h3>
                      <div class="stepper-desc">Country and phone</div>
                    </div>
                  </div>
                </div>
                <!--end::Step 2-->

                <!--begin::Step 3-->
                <div class="stepper-item" :class="{ current: currentStep === 3, completed: currentStep > 3 }">
                  <div class="stepper-wrapper d-flex align-items-center">
                    <div class="stepper-icon w-40px h-40px">
                      <i class="stepper-check fas fa-check"></i>
                      <span class="stepper-number">3</span>
                    </div>
                    <div class="stepper-label">
                      <h3 class="stepper-title">Address Details</h3>
                      <div class="stepper-desc">Full address info</div>
                    </div>
                  </div>
                </div>
                <!--end::Step 3-->
              </div>
              <!--end::Nav-->
            </div>
          </div>
          <!--begin::Aside-->

          <!--begin::Content-->
          <div class="d-flex flex-row-fluid flex-center">
            <div class="py-20 w-100 w-lg-700px px-9">
              <!--begin::Form-->
              <form class="my-auto pb-5" @submit.prevent="handleNext">
                
                <!--begin::Step 1-->
                <div v-if="currentStep === 1" class="pb-5">
                  <div class="w-100">
                    <div class="pb-10 pb-lg-15">
                      <h2 class="fw-bold text-dark">Basic Information</h2>
                      <div class="text-muted fw-semibold fs-6">
                        Enter the person's basic contact information.
                      </div>
                    </div>

                    <!--begin::Name fields-->
                    <div class="row g-9 mb-8">
                      <div class="col-md-6 fv-row">
                        <label class="required fs-6 fw-semibold mb-2">First Name</label>
                        <input
                          type="text"
                          class="form-control form-control-solid"
                          placeholder="First name"
                          v-model="formData.first_name"
                          :disabled="isSubmitting"
                        />
                      </div>
                      <div class="col-md-6 fv-row">
                        <label class="required fs-6 fw-semibold mb-2">Last Name</label>
                        <input
                          type="text"
                          class="form-control form-control-solid"
                          placeholder="Last name"
                          v-model="formData.last_name"
                          :disabled="isSubmitting"
                        />
                      </div>
                    </div>
                    <!--end::Name fields-->

                    <!--begin::Email-->
                    <div class="fv-row mb-8">
                      <label class="fs-6 fw-semibold mb-2">Email</label>
                      <input
                        type="email"
                        class="form-control form-control-solid"
                        placeholder="Email address"
                        v-model="formData.email"
                        :disabled="isSubmitting"
                      />
                    </div>
                    <!--end::Email-->

                    <!--begin::Personal Details-->
                    <div class="separator separator-content my-10">
                      <span class="w-250px fw-bold text-gray-600">Personal Details (Optional)</span>
                    </div>

                    <div class="row g-9 mb-8">
                      <div class="col-md-6 fv-row">
                        <label class="fs-6 fw-semibold mb-2">Date of Birth</label>
                        <input
                          type="date"
                          class="form-control form-control-solid"
                          v-model="formData.date_of_birth"
                          :disabled="isSubmitting"
                        />
                      </div>
                      <div class="col-md-6 fv-row">
                        <label class="fs-6 fw-semibold mb-2">Nationality</label>
                        <select
                          class="form-select form-select-solid"
                          v-model="formData.nationality"
                          :disabled="isSubmitting"
                        >
                          <option value="">Select nationality</option>
                          <option v-for="country in countries" :key="country.code" :value="country.nationality">
                            {{ country.nationality }}
                          </option>
                        </select>
                      </div>
                    </div>

                    <div class="row g-9 mb-8">
                      <div class="col-md-6 fv-row">
                        <label class="fs-6 fw-semibold mb-2">Passport Number</label>
                        <input
                          type="text"
                          class="form-control form-control-solid"
                          placeholder="Passport number"
                          v-model="formData.passport_number"
                          :disabled="isSubmitting"
                        />
                      </div>
                      <div class="col-md-6 fv-row">
                        <label class="fs-6 fw-semibold mb-2">Passport Expiration</label>
                        <input
                          type="date"
                          class="form-control form-control-solid"
                          v-model="formData.passport_expiration_date"
                          :disabled="isSubmitting"
                        />
                      </div>
                    </div>
                    <!--end::Personal Details-->
                  </div>
                </div>
                <!--end::Step 1-->

                <!--begin::Step 2-->
                <div v-if="currentStep === 2" class="pb-5">
                  <div class="w-100">
                    <div class="pb-10 pb-lg-15">
                      <h2 class="fw-bold text-dark">Phone & Location</h2>
                      <div class="text-muted fw-semibold fs-6">
                        Select country first for proper phone number formatting.
                      </div>
                    </div>

                    <!--begin::Country Selection-->
                    <div class="fv-row mb-8">
                      <label class="required fs-6 fw-semibold mb-2">Country</label>
                      <select
                        class="form-select form-select-solid"
                        v-model="formData.country"
                        @change="onCountryChange"
                        :disabled="isSubmitting"
                      >
                        <option value="">Select country</option>
                        <option v-for="country in countries" :key="country.code" :value="country.code">
                          {{ country.name }}
                        </option>
                      </select>
                      <div class="form-text">This will help format the phone number correctly.</div>
                    </div>
                    <!--end::Country Selection-->

                    <!--begin::Phone-->
                    <div class="fv-row mb-8">
                      <label class="fs-6 fw-semibold mb-2">Phone Number</label>
                      <input
                        type="tel"
                        class="form-control form-control-solid"
                        :placeholder="getPhonePlaceholder()"
                        v-model="formData.phone"
                        @input="formatPhoneNumber"
                        :disabled="isSubmitting"
                      />
                      <div class="text-muted fs-7 mt-1">
                        Phone will be formatted automatically based on selected country
                      </div>
                    </div>
                    <!--end::Phone-->
                  </div>
                </div>
                <!--end::Step 2-->

                <!--begin::Step 3-->
                <div v-if="currentStep === 3" class="pb-5">
                  <div class="w-100">
                    <div class="pb-10 pb-lg-15">
                      <h2 class="fw-bold text-dark">Address Details</h2>
                      <div class="text-muted fw-semibold fs-6">
                        Complete address information (optional).
                      </div>
                    </div>

                    <!--begin::Address-->
                    <div class="fv-row mb-8">
                      <label class="fs-6 fw-semibold mb-2">Address Line 1</label>
                      <input
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Street address"
                        v-model="formData.address_line1"
                        :disabled="isSubmitting"
                      />
                    </div>

                    <div class="fv-row mb-8">
                      <label class="fs-6 fw-semibold mb-2">Address Line 2</label>
                      <input
                        type="text"
                        class="form-control form-control-solid"
                        placeholder="Apartment, suite, etc."
                        v-model="formData.address_line2"
                        :disabled="isSubmitting"
                      />
                    </div>

                    <div class="row g-9 mb-8">
                      <div class="col-md-6 fv-row">
                        <label class="fs-6 fw-semibold mb-2">City</label>
                        <input
                          type="text"
                          class="form-control form-control-solid"
                          placeholder="City"
                          v-model="formData.city"
                          :disabled="isSubmitting"
                        />
                      </div>
                      <div class="col-md-3 fv-row">
                        <label class="fs-6 fw-semibold mb-2">State/Province</label>
                        <select
                          class="form-select form-select-solid"
                          v-model="formData.state"
                          :disabled="isSubmitting || (!formData.country || (formData.country !== 'US' && formData.country !== 'CA'))"
                        >
                          <option value="">Select state</option>
                          <option v-for="state in getStatesForCountry()" :key="state.code" :value="state.code">
                            {{ state.name }}
                          </option>
                        </select>
                      </div>
                      <div class="col-md-3 fv-row">
                        <label class="fs-6 fw-semibold mb-2">ZIP/Postal Code</label>
                        <input
                          type="text"
                          class="form-control form-control-solid"
                          :placeholder="getZipPlaceholder()"
                          v-model="formData.zip"
                          :disabled="isSubmitting"
                        />
                      </div>
                    </div>
                    <!--end::Address-->
                  </div>
                </div>
                <!--end::Step 3-->
              </form>
              <!--end::Form-->

              <!--begin::Actions-->
              <div class="d-flex flex-stack">
                <!--begin::Wrapper-->
                <div class="me-2">
                  <button
                    v-if="currentStep > 1"
                    type="button"
                    class="btn btn-lg btn-light-primary me-3"
                    @click="previousStep"
                    :disabled="isSubmitting"
                  >
                    <KTIcon icon-name="arrow-left" icon-class="fs-3 me-1" />
                    Back
                  </button>
                </div>
                <!--end::Wrapper-->

                <!--begin::Wrapper-->
                <div>
                  <button
                    v-if="currentStep < 3"
                    type="button"
                    class="btn btn-lg btn-primary me-3"
                    @click="nextStep"
                    :disabled="!isCurrentStepValid"
                  >
                    Continue
                    <KTIcon icon-name="arrow-right" icon-class="fs-3 ms-1" />
                  </button>

                  <button
                    v-if="currentStep === 3"
                    type="button"
                    class="btn btn-lg btn-primary"
                    @click="submitForm"
                    :disabled="isSubmitting || !isCurrentStepValid"
                  >
                    <span v-if="!isSubmitting" class="indicator-label">
                      Create Contact
                      <KTIcon icon-name="arrow-right" icon-class="fs-3 ms-2" />
                    </span>
                    <span v-else class="indicator-progress">
                      Creating...
                      <span class="spinner-border spinner-border-sm align-middle ms-2"></span>
                    </span>
                  </button>
                </div>
                <!--end::Wrapper-->
              </div>
              <!--end::Actions-->
            </div>
          </div>
          <!--end::Content-->
        </div>
        <!--end::Stepper-->
      </div>
      <!--end::Modal content-->
    </div>
    <!--end::Modal dialog-->
  </div>
  <!--end::Modal - Create contact-->
</template>

<script setup lang="ts">
import { ref, reactive, computed, nextTick, withDefaults, defineProps } from "vue";
import Swal from "sweetalert2";
import ApiService from "@/core/services/ApiService";
import { Modal } from "bootstrap";

// Props
interface Props {
  skipRoleSelection?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  skipRoleSelection: false,
});

const emit = defineEmits(['contactCreated', 'openPatientModal', 'openStaffModal', 'openPassengerModal']);

const modalRef = ref<HTMLElement | null>(null);
const isSubmitting = ref(false);
const currentStep = ref(1);

// Comprehensive country data
const countries = ref([
  { code: 'AF', name: 'Afghanistan', nationality: 'Afghan', phoneCode: '93' },
  { code: 'AL', name: 'Albania', nationality: 'Albanian', phoneCode: '355' },
  { code: 'DZ', name: 'Algeria', nationality: 'Algerian', phoneCode: '213' },
  { code: 'AD', name: 'Andorra', nationality: 'Andorran', phoneCode: '376' },
  { code: 'AO', name: 'Angola', nationality: 'Angolan', phoneCode: '244' },
  { code: 'AR', name: 'Argentina', nationality: 'Argentine', phoneCode: '54' },
  { code: 'AM', name: 'Armenia', nationality: 'Armenian', phoneCode: '374' },
  { code: 'AU', name: 'Australia', nationality: 'Australian', phoneCode: '61' },
  { code: 'AT', name: 'Austria', nationality: 'Austrian', phoneCode: '43' },
  { code: 'AZ', name: 'Azerbaijan', nationality: 'Azerbaijani', phoneCode: '994' },
  { code: 'BS', name: 'Bahamas', nationality: 'Bahamian', phoneCode: '1242' },
  { code: 'BH', name: 'Bahrain', nationality: 'Bahraini', phoneCode: '973' },
  { code: 'BD', name: 'Bangladesh', nationality: 'Bangladeshi', phoneCode: '880' },
  { code: 'BB', name: 'Barbados', nationality: 'Barbadian', phoneCode: '1246' },
  { code: 'BY', name: 'Belarus', nationality: 'Belarusian', phoneCode: '375' },
  { code: 'BE', name: 'Belgium', nationality: 'Belgian', phoneCode: '32' },
  { code: 'BZ', name: 'Belize', nationality: 'Belizean', phoneCode: '501' },
  { code: 'BJ', name: 'Benin', nationality: 'Beninese', phoneCode: '229' },
  { code: 'BT', name: 'Bhutan', nationality: 'Bhutanese', phoneCode: '975' },
  { code: 'BO', name: 'Bolivia', nationality: 'Bolivian', phoneCode: '591' },
  { code: 'BA', name: 'Bosnia and Herzegovina', nationality: 'Bosnian', phoneCode: '387' },
  { code: 'BW', name: 'Botswana', nationality: 'Botswanan', phoneCode: '267' },
  { code: 'BR', name: 'Brazil', nationality: 'Brazilian', phoneCode: '55' },
  { code: 'BN', name: 'Brunei', nationality: 'Bruneian', phoneCode: '673' },
  { code: 'BG', name: 'Bulgaria', nationality: 'Bulgarian', phoneCode: '359' },
  { code: 'BF', name: 'Burkina Faso', nationality: 'Burkinabe', phoneCode: '226' },
  { code: 'BI', name: 'Burundi', nationality: 'Burundian', phoneCode: '257' },
  { code: 'CV', name: 'Cape Verde', nationality: 'Cape Verdean', phoneCode: '238' },
  { code: 'KH', name: 'Cambodia', nationality: 'Cambodian', phoneCode: '855' },
  { code: 'CM', name: 'Cameroon', nationality: 'Cameroonian', phoneCode: '237' },
  { code: 'CA', name: 'Canada', nationality: 'Canadian', phoneCode: '1' },
  { code: 'CF', name: 'Central African Republic', nationality: 'Central African', phoneCode: '236' },
  { code: 'TD', name: 'Chad', nationality: 'Chadian', phoneCode: '235' },
  { code: 'CL', name: 'Chile', nationality: 'Chilean', phoneCode: '56' },
  { code: 'CN', name: 'China', nationality: 'Chinese', phoneCode: '86' },
  { code: 'CO', name: 'Colombia', nationality: 'Colombian', phoneCode: '57' },
  { code: 'KM', name: 'Comoros', nationality: 'Comoran', phoneCode: '269' },
  { code: 'CG', name: 'Congo', nationality: 'Congolese', phoneCode: '242' },
  { code: 'CR', name: 'Costa Rica', nationality: 'Costa Rican', phoneCode: '506' },
  { code: 'HR', name: 'Croatia', nationality: 'Croatian', phoneCode: '385' },
  { code: 'CU', name: 'Cuba', nationality: 'Cuban', phoneCode: '53' },
  { code: 'CY', name: 'Cyprus', nationality: 'Cypriot', phoneCode: '357' },
  { code: 'CZ', name: 'Czech Republic', nationality: 'Czech', phoneCode: '420' },
  { code: 'DK', name: 'Denmark', nationality: 'Danish', phoneCode: '45' },
  { code: 'DJ', name: 'Djibouti', nationality: 'Djiboutian', phoneCode: '253' },
  { code: 'DM', name: 'Dominica', nationality: 'Dominican', phoneCode: '1767' },
  { code: 'DO', name: 'Dominican Republic', nationality: 'Dominican', phoneCode: '1809' },
  { code: 'EC', name: 'Ecuador', nationality: 'Ecuadorian', phoneCode: '593' },
  { code: 'EG', name: 'Egypt', nationality: 'Egyptian', phoneCode: '20' },
  { code: 'SV', name: 'El Salvador', nationality: 'Salvadoran', phoneCode: '503' },
  { code: 'GQ', name: 'Equatorial Guinea', nationality: 'Equatorial Guinean', phoneCode: '240' },
  { code: 'ER', name: 'Eritrea', nationality: 'Eritrean', phoneCode: '291' },
  { code: 'EE', name: 'Estonia', nationality: 'Estonian', phoneCode: '372' },
  { code: 'SZ', name: 'Eswatini', nationality: 'Swazi', phoneCode: '268' },
  { code: 'ET', name: 'Ethiopia', nationality: 'Ethiopian', phoneCode: '251' },
  { code: 'FJ', name: 'Fiji', nationality: 'Fijian', phoneCode: '679' },
  { code: 'FI', name: 'Finland', nationality: 'Finnish', phoneCode: '358' },
  { code: 'FR', name: 'France', nationality: 'French', phoneCode: '33' },
  { code: 'GA', name: 'Gabon', nationality: 'Gabonese', phoneCode: '241' },
  { code: 'GM', name: 'Gambia', nationality: 'Gambian', phoneCode: '220' },
  { code: 'GE', name: 'Georgia', nationality: 'Georgian', phoneCode: '995' },
  { code: 'DE', name: 'Germany', nationality: 'German', phoneCode: '49' },
  { code: 'GH', name: 'Ghana', nationality: 'Ghanaian', phoneCode: '233' },
  { code: 'GR', name: 'Greece', nationality: 'Greek', phoneCode: '30' },
  { code: 'GD', name: 'Grenada', nationality: 'Grenadian', phoneCode: '1473' },
  { code: 'GT', name: 'Guatemala', nationality: 'Guatemalan', phoneCode: '502' },
  { code: 'GN', name: 'Guinea', nationality: 'Guinean', phoneCode: '224' },
  { code: 'GW', name: 'Guinea-Bissau', nationality: 'Guinea-Bissauan', phoneCode: '245' },
  { code: 'GY', name: 'Guyana', nationality: 'Guyanese', phoneCode: '592' },
  { code: 'HT', name: 'Haiti', nationality: 'Haitian', phoneCode: '509' },
  { code: 'HN', name: 'Honduras', nationality: 'Honduran', phoneCode: '504' },
  { code: 'HU', name: 'Hungary', nationality: 'Hungarian', phoneCode: '36' },
  { code: 'IS', name: 'Iceland', nationality: 'Icelandic', phoneCode: '354' },
  { code: 'IN', name: 'India', nationality: 'Indian', phoneCode: '91' },
  { code: 'ID', name: 'Indonesia', nationality: 'Indonesian', phoneCode: '62' },
  { code: 'IR', name: 'Iran', nationality: 'Iranian', phoneCode: '98' },
  { code: 'IQ', name: 'Iraq', nationality: 'Iraqi', phoneCode: '964' },
  { code: 'IE', name: 'Ireland', nationality: 'Irish', phoneCode: '353' },
  { code: 'IL', name: 'Israel', nationality: 'Israeli', phoneCode: '972' },
  { code: 'IT', name: 'Italy', nationality: 'Italian', phoneCode: '39' },
  { code: 'CI', name: 'Ivory Coast', nationality: 'Ivorian', phoneCode: '225' },
  { code: 'JM', name: 'Jamaica', nationality: 'Jamaican', phoneCode: '1876' },
  { code: 'JP', name: 'Japan', nationality: 'Japanese', phoneCode: '81' },
  { code: 'JO', name: 'Jordan', nationality: 'Jordanian', phoneCode: '962' },
  { code: 'KZ', name: 'Kazakhstan', nationality: 'Kazakhstani', phoneCode: '7' },
  { code: 'KE', name: 'Kenya', nationality: 'Kenyan', phoneCode: '254' },
  { code: 'KI', name: 'Kiribati', nationality: 'I-Kiribati', phoneCode: '686' },
  { code: 'KP', name: 'North Korea', nationality: 'North Korean', phoneCode: '850' },
  { code: 'KR', name: 'South Korea', nationality: 'South Korean', phoneCode: '82' },
  { code: 'KW', name: 'Kuwait', nationality: 'Kuwaiti', phoneCode: '965' },
  { code: 'KG', name: 'Kyrgyzstan', nationality: 'Kyrgyzstani', phoneCode: '996' },
  { code: 'LA', name: 'Laos', nationality: 'Laotian', phoneCode: '856' },
  { code: 'LV', name: 'Latvia', nationality: 'Latvian', phoneCode: '371' },
  { code: 'LB', name: 'Lebanon', nationality: 'Lebanese', phoneCode: '961' },
  { code: 'LS', name: 'Lesotho', nationality: 'Basotho', phoneCode: '266' },
  { code: 'LR', name: 'Liberia', nationality: 'Liberian', phoneCode: '231' },
  { code: 'LY', name: 'Libya', nationality: 'Libyan', phoneCode: '218' },
  { code: 'LI', name: 'Liechtenstein', nationality: 'Liechtensteiner', phoneCode: '423' },
  { code: 'LT', name: 'Lithuania', nationality: 'Lithuanian', phoneCode: '370' },
  { code: 'LU', name: 'Luxembourg', nationality: 'Luxembourgish', phoneCode: '352' },
  { code: 'MG', name: 'Madagascar', nationality: 'Malagasy', phoneCode: '261' },
  { code: 'MW', name: 'Malawi', nationality: 'Malawian', phoneCode: '265' },
  { code: 'MY', name: 'Malaysia', nationality: 'Malaysian', phoneCode: '60' },
  { code: 'MV', name: 'Maldives', nationality: 'Maldivian', phoneCode: '960' },
  { code: 'ML', name: 'Mali', nationality: 'Malian', phoneCode: '223' },
  { code: 'MT', name: 'Malta', nationality: 'Maltese', phoneCode: '356' },
  { code: 'MH', name: 'Marshall Islands', nationality: 'Marshallese', phoneCode: '692' },
  { code: 'MR', name: 'Mauritania', nationality: 'Mauritanian', phoneCode: '222' },
  { code: 'MU', name: 'Mauritius', nationality: 'Mauritian', phoneCode: '230' },
  { code: 'MX', name: 'Mexico', nationality: 'Mexican', phoneCode: '52' },
  { code: 'FM', name: 'Micronesia', nationality: 'Micronesian', phoneCode: '691' },
  { code: 'MD', name: 'Moldova', nationality: 'Moldovan', phoneCode: '373' },
  { code: 'MC', name: 'Monaco', nationality: 'Monégasque', phoneCode: '377' },
  { code: 'MN', name: 'Mongolia', nationality: 'Mongolian', phoneCode: '976' },
  { code: 'ME', name: 'Montenegro', nationality: 'Montenegrin', phoneCode: '382' },
  { code: 'MA', name: 'Morocco', nationality: 'Moroccan', phoneCode: '212' },
  { code: 'MZ', name: 'Mozambique', nationality: 'Mozambican', phoneCode: '258' },
  { code: 'MM', name: 'Myanmar', nationality: 'Burmese', phoneCode: '95' },
  { code: 'NA', name: 'Namibia', nationality: 'Namibian', phoneCode: '264' },
  { code: 'NR', name: 'Nauru', nationality: 'Nauruan', phoneCode: '674' },
  { code: 'NP', name: 'Nepal', nationality: 'Nepali', phoneCode: '977' },
  { code: 'NL', name: 'Netherlands', nationality: 'Dutch', phoneCode: '31' },
  { code: 'NZ', name: 'New Zealand', nationality: 'New Zealand', phoneCode: '64' },
  { code: 'NI', name: 'Nicaragua', nationality: 'Nicaraguan', phoneCode: '505' },
  { code: 'NE', name: 'Niger', nationality: 'Nigerien', phoneCode: '227' },
  { code: 'NG', name: 'Nigeria', nationality: 'Nigerian', phoneCode: '234' },
  { code: 'MK', name: 'North Macedonia', nationality: 'Macedonian', phoneCode: '389' },
  { code: 'NO', name: 'Norway', nationality: 'Norwegian', phoneCode: '47' },
  { code: 'OM', name: 'Oman', nationality: 'Omani', phoneCode: '968' },
  { code: 'PK', name: 'Pakistan', nationality: 'Pakistani', phoneCode: '92' },
  { code: 'PW', name: 'Palau', nationality: 'Palauan', phoneCode: '680' },
  { code: 'PS', name: 'Palestine', nationality: 'Palestinian', phoneCode: '970' },
  { code: 'PA', name: 'Panama', nationality: 'Panamanian', phoneCode: '507' },
  { code: 'PG', name: 'Papua New Guinea', nationality: 'Papua New Guinean', phoneCode: '675' },
  { code: 'PY', name: 'Paraguay', nationality: 'Paraguayan', phoneCode: '595' },
  { code: 'PE', name: 'Peru', nationality: 'Peruvian', phoneCode: '51' },
  { code: 'PH', name: 'Philippines', nationality: 'Filipino', phoneCode: '63' },
  { code: 'PL', name: 'Poland', nationality: 'Polish', phoneCode: '48' },
  { code: 'PT', name: 'Portugal', nationality: 'Portuguese', phoneCode: '351' },
  { code: 'QA', name: 'Qatar', nationality: 'Qatari', phoneCode: '974' },
  { code: 'RO', name: 'Romania', nationality: 'Romanian', phoneCode: '40' },
  { code: 'RU', name: 'Russia', nationality: 'Russian', phoneCode: '7' },
  { code: 'RW', name: 'Rwanda', nationality: 'Rwandan', phoneCode: '250' },
  { code: 'KN', name: 'Saint Kitts and Nevis', nationality: 'Kittitian', phoneCode: '1869' },
  { code: 'LC', name: 'Saint Lucia', nationality: 'Saint Lucian', phoneCode: '1758' },
  { code: 'VC', name: 'Saint Vincent and the Grenadines', nationality: 'Vincentian', phoneCode: '1784' },
  { code: 'WS', name: 'Samoa', nationality: 'Samoan', phoneCode: '685' },
  { code: 'SM', name: 'San Marino', nationality: 'Sammarinese', phoneCode: '378' },
  { code: 'ST', name: 'São Tomé and Príncipe', nationality: 'São Toméan', phoneCode: '239' },
  { code: 'SA', name: 'Saudi Arabia', nationality: 'Saudi', phoneCode: '966' },
  { code: 'SN', name: 'Senegal', nationality: 'Senegalese', phoneCode: '221' },
  { code: 'RS', name: 'Serbia', nationality: 'Serbian', phoneCode: '381' },
  { code: 'SC', name: 'Seychelles', nationality: 'Seychellois', phoneCode: '248' },
  { code: 'SL', name: 'Sierra Leone', nationality: 'Sierra Leonean', phoneCode: '232' },
  { code: 'SG', name: 'Singapore', nationality: 'Singaporean', phoneCode: '65' },
  { code: 'SK', name: 'Slovakia', nationality: 'Slovak', phoneCode: '421' },
  { code: 'SI', name: 'Slovenia', nationality: 'Slovenian', phoneCode: '386' },
  { code: 'SB', name: 'Solomon Islands', nationality: 'Solomon Islander', phoneCode: '677' },
  { code: 'SO', name: 'Somalia', nationality: 'Somali', phoneCode: '252' },
  { code: 'ZA', name: 'South Africa', nationality: 'South African', phoneCode: '27' },
  { code: 'SS', name: 'South Sudan', nationality: 'South Sudanese', phoneCode: '211' },
  { code: 'ES', name: 'Spain', nationality: 'Spanish', phoneCode: '34' },
  { code: 'LK', name: 'Sri Lanka', nationality: 'Sri Lankan', phoneCode: '94' },
  { code: 'SD', name: 'Sudan', nationality: 'Sudanese', phoneCode: '249' },
  { code: 'SR', name: 'Suriname', nationality: 'Surinamese', phoneCode: '597' },
  { code: 'SE', name: 'Sweden', nationality: 'Swedish', phoneCode: '46' },
  { code: 'CH', name: 'Switzerland', nationality: 'Swiss', phoneCode: '41' },
  { code: 'SY', name: 'Syria', nationality: 'Syrian', phoneCode: '963' },
  { code: 'TW', name: 'Taiwan', nationality: 'Taiwanese', phoneCode: '886' },
  { code: 'TJ', name: 'Tajikistan', nationality: 'Tajikistani', phoneCode: '992' },
  { code: 'TZ', name: 'Tanzania', nationality: 'Tanzanian', phoneCode: '255' },
  { code: 'TH', name: 'Thailand', nationality: 'Thai', phoneCode: '66' },
  { code: 'TL', name: 'Timor-Leste', nationality: 'Timorese', phoneCode: '670' },
  { code: 'TG', name: 'Togo', nationality: 'Togolese', phoneCode: '228' },
  { code: 'TO', name: 'Tonga', nationality: 'Tongan', phoneCode: '676' },
  { code: 'TT', name: 'Trinidad and Tobago', nationality: 'Trinidadian', phoneCode: '1868' },
  { code: 'TN', name: 'Tunisia', nationality: 'Tunisian', phoneCode: '216' },
  { code: 'TR', name: 'Turkey', nationality: 'Turkish', phoneCode: '90' },
  { code: 'TM', name: 'Turkmenistan', nationality: 'Turkmen', phoneCode: '993' },
  { code: 'TV', name: 'Tuvalu', nationality: 'Tuvaluan', phoneCode: '688' },
  { code: 'UG', name: 'Uganda', nationality: 'Ugandan', phoneCode: '256' },
  { code: 'UA', name: 'Ukraine', nationality: 'Ukrainian', phoneCode: '380' },
  { code: 'AE', name: 'United Arab Emirates', nationality: 'Emirati', phoneCode: '971' },
  { code: 'GB', name: 'United Kingdom', nationality: 'British', phoneCode: '44' },
  { code: 'US', name: 'United States', nationality: 'American', phoneCode: '1' },
  { code: 'UY', name: 'Uruguay', nationality: 'Uruguayan', phoneCode: '598' },
  { code: 'UZ', name: 'Uzbekistan', nationality: 'Uzbekistani', phoneCode: '998' },
  { code: 'VU', name: 'Vanuatu', nationality: 'Vanuatuan', phoneCode: '678' },
  { code: 'VA', name: 'Vatican City', nationality: 'Vatican', phoneCode: '379' },
  { code: 'VE', name: 'Venezuela', nationality: 'Venezuelan', phoneCode: '58' },
  { code: 'VN', name: 'Vietnam', nationality: 'Vietnamese', phoneCode: '84' },
  { code: 'YE', name: 'Yemen', nationality: 'Yemeni', phoneCode: '967' },
  { code: 'ZM', name: 'Zambia', nationality: 'Zambian', phoneCode: '260' },
  { code: 'ZW', name: 'Zimbabwe', nationality: 'Zimbabwean', phoneCode: '263' },
]);

const states = ref([
  // US States
  { code: 'AL', name: 'Alabama', country: 'US' },
  { code: 'AK', name: 'Alaska', country: 'US' },
  { code: 'AZ', name: 'Arizona', country: 'US' },
  { code: 'AR', name: 'Arkansas', country: 'US' },
  { code: 'CA', name: 'California', country: 'US' },
  { code: 'CO', name: 'Colorado', country: 'US' },
  { code: 'CT', name: 'Connecticut', country: 'US' },
  { code: 'DE', name: 'Delaware', country: 'US' },
  { code: 'FL', name: 'Florida', country: 'US' },
  { code: 'GA', name: 'Georgia', country: 'US' },
  { code: 'HI', name: 'Hawaii', country: 'US' },
  { code: 'ID', name: 'Idaho', country: 'US' },
  { code: 'IL', name: 'Illinois', country: 'US' },
  { code: 'IN', name: 'Indiana', country: 'US' },
  { code: 'IA', name: 'Iowa', country: 'US' },
  { code: 'KS', name: 'Kansas', country: 'US' },
  { code: 'KY', name: 'Kentucky', country: 'US' },
  { code: 'LA', name: 'Louisiana', country: 'US' },
  { code: 'ME', name: 'Maine', country: 'US' },
  { code: 'MD', name: 'Maryland', country: 'US' },
  { code: 'MA', name: 'Massachusetts', country: 'US' },
  { code: 'MI', name: 'Michigan', country: 'US' },
  { code: 'MN', name: 'Minnesota', country: 'US' },
  { code: 'MS', name: 'Mississippi', country: 'US' },
  { code: 'MO', name: 'Missouri', country: 'US' },
  { code: 'MT', name: 'Montana', country: 'US' },
  { code: 'NE', name: 'Nebraska', country: 'US' },
  { code: 'NV', name: 'Nevada', country: 'US' },
  { code: 'NH', name: 'New Hampshire', country: 'US' },
  { code: 'NJ', name: 'New Jersey', country: 'US' },
  { code: 'NM', name: 'New Mexico', country: 'US' },
  { code: 'NY', name: 'New York', country: 'US' },
  { code: 'NC', name: 'North Carolina', country: 'US' },
  { code: 'ND', name: 'North Dakota', country: 'US' },
  { code: 'OH', name: 'Ohio', country: 'US' },
  { code: 'OK', name: 'Oklahoma', country: 'US' },
  { code: 'OR', name: 'Oregon', country: 'US' },
  { code: 'PA', name: 'Pennsylvania', country: 'US' },
  { code: 'RI', name: 'Rhode Island', country: 'US' },
  { code: 'SC', name: 'South Carolina', country: 'US' },
  { code: 'SD', name: 'South Dakota', country: 'US' },
  { code: 'TN', name: 'Tennessee', country: 'US' },
  { code: 'TX', name: 'Texas', country: 'US' },
  { code: 'UT', name: 'Utah', country: 'US' },
  { code: 'VT', name: 'Vermont', country: 'US' },
  { code: 'VA', name: 'Virginia', country: 'US' },
  { code: 'WA', name: 'Washington', country: 'US' },
  { code: 'WV', name: 'West Virginia', country: 'US' },
  { code: 'WI', name: 'Wisconsin', country: 'US' },
  { code: 'WY', name: 'Wyoming', country: 'US' },
  { code: 'DC', name: 'District of Columbia', country: 'US' },
  // Canadian provinces
  { code: 'AB', name: 'Alberta', country: 'CA' },
  { code: 'BC', name: 'British Columbia', country: 'CA' },
  { code: 'MB', name: 'Manitoba', country: 'CA' },
  { code: 'NB', name: 'New Brunswick', country: 'CA' },
  { code: 'NL', name: 'Newfoundland and Labrador', country: 'CA' },
  { code: 'NS', name: 'Nova Scotia', country: 'CA' },
  { code: 'ON', name: 'Ontario', country: 'CA' },
  { code: 'PE', name: 'Prince Edward Island', country: 'CA' },
  { code: 'QC', name: 'Quebec', country: 'CA' },
  { code: 'SK', name: 'Saskatchewan', country: 'CA' },
  { code: 'NT', name: 'Northwest Territories', country: 'CA' },
  { code: 'NU', name: 'Nunavut', country: 'CA' },
  { code: 'YT', name: 'Yukon', country: 'CA' },
]);

// Form data
const formData = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  zip: '',
  country: '',
  date_of_birth: '',
  nationality: '',
  passport_number: '',
  passport_expiration_date: '',
});

// Computed validations
const isCurrentStepValid = computed(() => {
  switch (currentStep.value) {
    case 1:
      return !!formData.first_name && !!formData.last_name;
    case 2:
      return !!formData.country;
    case 3:
      return true; // Address step is optional
    default:
      return false;
  }
});

// Methods
const getStatesForCountry = () => {
  return states.value.filter(state => state.country === formData.country);
};

const getZipPlaceholder = (): string => {
  const placeholders: Record<string, string> = {
    'US': '12345',
    'CA': 'K1A 0A6',
    'GB': 'SW1A 1AA',
    'DE': '10115',
    'FR': '75001',
    'AU': '2000',
    'JP': '100-0001',
  };
  return placeholders[formData.country] || 'Postal Code';
};

const resetForm = () => {
  Object.assign(formData, {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    zip: '',
    country: '',
    date_of_birth: '',
    nationality: '',
    passport_number: '',
    passport_expiration_date: '',
  });
  
  currentStep.value = 1;
};

const nextStep = () => {
  if (isCurrentStepValid.value && currentStep.value < 3) {
    currentStep.value++;
  }
};

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const formatPhoneNumber = (event: Event) => {
  const input = event.target as HTMLInputElement;
  let value = input.value.replace(/\D/g, '');
  
  if (!value) {
    formData.phone = '';
    return;
  }
  
  const selectedCountry = countries.value.find(c => c.code === formData.country);
  const defaultCountryCode = selectedCountry?.phoneCode || '1';
  
  let countryCode = defaultCountryCode;
  let nationalNumber = value;
  
  for (const country of countries.value) {
    if (value.startsWith(country.phoneCode)) {
      countryCode = country.phoneCode;
      nationalNumber = value.slice(country.phoneCode.length);
      break;
    }
  }
  
  let formattedNumber = '';
  
  if (countryCode === '1') {
    if (nationalNumber.length >= 10) {
      const areaCode = nationalNumber.slice(0, 3);
      const exchange = nationalNumber.slice(3, 6);
      const number = nationalNumber.slice(6, 10);
      formattedNumber = `+1 (${areaCode}) ${exchange}-${number}`;
    } else if (nationalNumber.length >= 7) {
      const exchange = nationalNumber.slice(0, 3);
      const number = nationalNumber.slice(3);
      formattedNumber = `+1 ${exchange}-${number}`;
    } else if (nationalNumber.length >= 3) {
      const areaCode = nationalNumber.slice(0, 3);
      const rest = nationalNumber.slice(3);
      formattedNumber = `+1 (${areaCode}) ${rest}`;
    } else {
      formattedNumber = `+1 ${nationalNumber}`;
    }
  } else {
    if (nationalNumber.length >= 8) {
      const parts = [];
      let remaining = nationalNumber;
      
      while (remaining.length > 0) {
        if (remaining.length <= 4) {
          parts.push(remaining);
          break;
        } else {
          parts.push(remaining.slice(0, 3));
          remaining = remaining.slice(3);
        }
      }
      formattedNumber = `+${countryCode} ${parts.join(' ')}`;
    } else {
      formattedNumber = `+${countryCode} ${nationalNumber}`;
    }
  }
  
  formData.phone = formattedNumber;
};

const onCountryChange = () => {
  if (formData.country !== 'US' && formData.country !== 'CA') {
    formData.state = '';
  }
  
  if (formData.phone && formData.phone.length > 0) {
    const numbers = formData.phone.replace(/\D/g, '');
    if (numbers.length > 0) {
      const mockEvent = {
        target: { value: numbers }
      } as unknown as Event;
      formatPhoneNumber(mockEvent);
    }
  }
};

const getPhonePlaceholder = (): string => {
  const selectedCountry = countries.value.find(c => c.code === formData.country);
  const phoneCode = selectedCountry?.phoneCode || '1';
  
  const placeholders: Record<string, string> = {
    '1': '+1 (555) 123-4567',
    '44': '+44 20 7946 0958',
    '49': '+49 30 12345678',
    '33': '+33 1 42 86 83 26',
    '61': '+61 2 9876 5432',
    '81': '+81 3 1234 5678',
    '86': '+86 138 0013 8000',
    '91': '+91 98765 43210',
    '55': '+55 11 99999 9999',
  };
  
  return placeholders[phoneCode] || `+${phoneCode} XXX XXX XXXX`;
};

const openPatientModal = (contact: any) => {
  // Emit event to parent to handle patient modal opening
  emit('openPatientModal', contact);
};

const openStaffModal = (contact: any) => {
  // Emit event to parent to handle staff modal opening
  emit('openStaffModal', contact);
};

const openPassengerModal = (contact: any) => {
  // Emit event to parent to handle passenger modal opening
  emit('openPassengerModal', contact);
};

const promptForRoleConversion = async (contact: any) => {
  const result = await Swal.fire({
    title: "Convert Contact to Role",
    html: `
      <div class="text-start">
        <p><strong>Contact:</strong> ${contact.first_name} ${contact.last_name}</p>
        <p>Would you like to assign a specific role to this contact?</p>
        <div class="mt-4">
          <button type="button" class="btn btn-primary btn-sm me-2" data-result="staff">
            <i class="ki-duotone ki-user fs-5 me-1"><span class="path1"></span><span class="path2"></span></i>
            Staff Member
          </button>
          <button type="button" class="btn btn-success btn-sm me-2" data-result="patient">
            <i class="ki-duotone ki-heart fs-5 me-1"><span class="path1"></span><span class="path2"></span><span class="path3"></span></i>
            Patient
          </button>
          <button type="button" class="btn btn-info btn-sm me-2" data-result="passenger">
            <i class="ki-duotone ki-people fs-5 me-1"><span class="path1"></span><span class="path2"></span><span class="path3"></span><span class="path4"></span><span class="path5"></span></i>
            Passenger
          </button>
          <button type="button" class="btn btn-secondary btn-sm" data-result="customer">
            <i class="ki-duotone ki-handshake fs-5 me-1"><span class="path1"></span><span class="path2"></span></i>
            Customer Only
          </button>
        </div>
      </div>
    `,
    showConfirmButton: false,
    showCancelButton: true,
    cancelButtonText: "Skip for Now",
    didOpen: () => {
      const buttons = document.querySelectorAll('[data-result]');
      buttons.forEach(button => {
        button.addEventListener('click', (e) => {
          const result = (e.target as HTMLElement).closest('[data-result]')?.getAttribute('data-result');
          Swal.close();
          handleRoleSelection(result, contact);
        });
      });
    }
  });

  if (result.dismiss === Swal.DismissReason.cancel) {
    // User chose to skip role assignment
    Swal.fire({
      title: "Success!",
      text: "Contact created successfully! You can assign roles later from the Contacts page.",
      icon: "success",
      confirmButtonText: "OK"
    });
  }
};

const handleRoleSelection = (roleType: string | null, contact: any) => {
  switch (roleType) {
    case 'staff':
      openStaffModal(contact);
      break;
    case 'patient':
      openPatientModal(contact);
      break;
    case 'passenger':
      openPassengerModal(contact);
      break;
    case 'customer':
      Swal.fire({
        title: "Success!",
        text: "Contact created successfully as a customer!",
        icon: "success",
        confirmButtonText: "OK"
      });
      break;
  }
};

const submitForm = async () => {
  if (!isCurrentStepValid.value || isSubmitting.value) return;
  
  isSubmitting.value = true;
  
  try {
    const contactData = {
      first_name: formData.first_name,
      last_name: formData.last_name,
      business_name: null,
      email: formData.email || null,
      phone: formData.phone || null,
      address_line1: formData.address_line1 || null,
      address_line2: formData.address_line2 || null,
      city: formData.city || null,
      state: formData.state || null,
      zip: formData.zip || null,
      country: formData.country || null,
      date_of_birth: formData.date_of_birth || null,
      nationality: formData.nationality || null,
      passport_number: formData.passport_number || null,
      passport_expiration_date: formData.passport_expiration_date || null,
    };
    
    console.log('Creating contact:', contactData);
    
    const response = await ApiService.post("/contacts/", contactData);
    const newContact = response.data;
    
    emit('contactCreated', newContact);
    
    // Reset form
    resetForm();
    
    // Force close modal using multiple methods
    const modalElement = document.getElementById('kt_modal_create_contact');
    if (modalElement) {
      // Method 1: Try Bootstrap modal instance
      try {
        if ((window as any).bootstrap?.Modal) {
          const modal = (window as any).bootstrap.Modal.getInstance(modalElement) || 
                       new (window as any).bootstrap.Modal(modalElement);
          modal.hide();
        }
      } catch (error) {
        console.log('Bootstrap modal hide failed:', error);
      }
      
      // Method 2: Force hide with direct DOM manipulation
      modalElement.classList.remove('show');
      modalElement.style.display = 'none';
      modalElement.setAttribute('aria-hidden', 'true');
      modalElement.removeAttribute('aria-modal');
      modalElement.removeAttribute('role');
    }
    
    // Method 3: Clean up all modal artifacts immediately
    setTimeout(() => {
      // Remove all modal backdrops
      const backdrops = document.querySelectorAll('.modal-backdrop');
      backdrops.forEach(backdrop => backdrop.remove());
      
      // Remove modal-open class from body and reset styles
      document.body.classList.remove('modal-open');
      document.body.style.removeProperty('overflow');
      document.body.style.removeProperty('padding-right');
      
      // Remove any aria-hidden from app
      const app = document.getElementById('app');
      if (app) {
        app.removeAttribute('aria-hidden');
      }
    }, 50);
    
    // Show role conversion prompt after modal starts closing (unless skipped)
    if (!props.skipRoleSelection) {
      setTimeout(() => {
        promptForRoleConversion(newContact);
      }, 100);
    }
    
  } catch (error: any) {
    console.error('Error creating contact:', error);
    
    let errorMessage = "Failed to create contact. Please try again.";
    
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.response?.data) {
      const errors = error.response.data;
      const errorMessages = [];
      
      for (const field in errors) {
        if (Array.isArray(errors[field])) {
          errorMessages.push(`${field}: ${errors[field].join(', ')}`);
        } else {
          errorMessages.push(`${field}: ${errors[field]}`);
        }
      }
      
      if (errorMessages.length > 0) {
        errorMessage = errorMessages.join('\n');
      }
    }
    
    Swal.fire({
      title: "Error!",
      text: errorMessage,
      icon: "error",
      confirmButtonText: "OK"
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.stepper-item.current .stepper-wrapper .stepper-icon {
  background-color: var(--bs-primary);
  color: white;
}

.stepper-item.completed .stepper-wrapper .stepper-icon {
  background-color: var(--bs-success);
  color: white;
}

.stepper-item.completed .stepper-wrapper .stepper-icon .stepper-number {
  display: none;
}

.stepper-item.completed .stepper-wrapper .stepper-icon .stepper-check {
  display: inline;
}

.stepper-item .stepper-wrapper .stepper-icon .stepper-check {
  display: none;
}

.separator-content {
  position: relative;
  z-index: 1;
}

.separator-content span {
  background: var(--bs-body-bg);
  padding: 0 1rem;
}
</style>