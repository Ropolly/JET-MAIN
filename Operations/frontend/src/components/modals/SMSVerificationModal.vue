<template>
  <div class="modal fade" id="sms-verification-modal" tabindex="-1" aria-labelledby="smsVerificationModalLabel" aria-hidden="true" ref="modalElement">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="smsVerificationModalLabel">
            {{ title }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
            @click="handleClose"
          ></button>
        </div>

        <div class="modal-body">
          <div v-if="!showCodeInput" class="text-center">
            <!-- Phone Number Entry Step -->
            <div class="mb-4">
              <i class="fas fa-mobile-alt text-primary mb-3" style="font-size: 2.5rem;"></i>
              <p class="text-muted">
                {{ phoneInputMessage }}
              </p>
            </div>

            <PhoneNumberInput
              v-model="phoneNumber"
              :required="true"
              :auto-format="true"
              :validate-on-input="true"
              placeholder="(555) 123-4567"
              @validation-change="handlePhoneValidation"
              ref="phoneInputRef"
            />

            <div v-if="phoneError" class="alert alert-danger">
              {{ phoneError }}
            </div>
          </div>

          <div v-else class="text-center">
            <!-- SMS Code Entry Step -->
            <div class="mb-4">
              <i class="fas fa-comment-sms text-success mb-3" style="font-size: 2.5rem;"></i>
              <p class="text-muted">
                We've sent a verification code to<br>
                <strong>{{ maskedPhoneNumber }}</strong>
              </p>
              <p class="text-sm text-muted">
                Enter the 6-digit code below
              </p>
            </div>

            <div class="mb-4">
              <label class="form-label fw-semibold fs-6 required">Verification Code</label>
              <input
                ref="codeInputRef"
                type="text"
                class="form-control form-control-solid text-center fs-2 letter-spacing-2"
                :class="{ 'is-invalid': codeError }"
                v-model="verificationCode"
                @input="handleCodeInput"
                @keypress="handleCodeKeypress"
                placeholder="000000"
                maxlength="6"
                autocomplete="one-time-code"
                style="font-family: monospace; letter-spacing: 0.5rem;"
              />
              <div v-if="codeError" class="invalid-feedback">
                {{ codeError }}
              </div>
            </div>

            <!-- Countdown Timer and Resend -->
            <div class="mb-3">
              <div v-if="countdown > 0" class="text-muted">
                <i class="fas fa-clock me-2"></i>
                Resend code in {{ countdown }}s
              </div>
              <div v-else>
                <button
                  type="button"
                  class="btn btn-link text-primary p-0"
                  @click="resendCode"
                  :disabled="sendingCode"
                >
                  <i class="fas fa-redo me-2" :class="{ 'fa-spin': sendingCode }"></i>
                  {{ sendingCode ? 'Sending...' : 'Send Another Code' }}
                </button>
              </div>
            </div>

            <!-- Edit Phone Number Link -->
            <button
              type="button"
              class="btn btn-link text-muted p-0 text-decoration-underline"
              @click="editPhoneNumber"
            >
              <i class="fas fa-edit me-1"></i>
              Edit phone number
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-3">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted mt-2">{{ loadingMessage }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="handleClose"
            :disabled="loading"
          >
            {{ showCodeInput ? 'Cancel' : 'Cancel' }}
          </button>

          <button
            v-if="!showCodeInput"
            type="button"
            class="btn btn-primary"
            @click="sendVerificationCode"
            :disabled="!isPhoneValid || sendingCode || loading"
          >
            <i v-if="sendingCode" class="fas fa-spinner fa-spin me-2"></i>
            <i v-else class="fas fa-paper-plane me-2"></i>
            {{ sendingCode ? 'Sending...' : 'Send Code' }}
          </button>

          <button
            v-else
            type="button"
            class="btn btn-primary"
            @click="verifyCode"
            :disabled="!isCodeValid || verifyingCode || loading"
          >
            <i v-if="verifyingCode" class="fas fa-spinner fa-spin me-2"></i>
            <i v-else class="fas fa-check me-2"></i>
            {{ verifyingCode ? 'Verifying...' : 'Verify Code' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { Modal } from 'bootstrap'
import PhoneNumberInput from '@/components/forms/PhoneNumberInput.vue'
import Swal from 'sweetalert2'

interface Props {
  title?: string
  phoneInputMessage?: string
  autoShow?: boolean
  allowPhoneEdit?: boolean
  initialPhoneNumber?: string
}

interface Emits {
  (e: 'phone-verified', data: { phoneNumber: string, verificationCode: string }): void
  (e: 'closed'): void
  (e: 'phone-sent', phoneNumber: string): void
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Verify Phone Number',
  phoneInputMessage: 'Enter your phone number to receive a verification code',
  autoShow: false,
  allowPhoneEdit: true,
  initialPhoneNumber: ''
})

const emit = defineEmits<Emits>()

// Template refs
const modalElement = ref<HTMLElement | null>(null)
const phoneInputRef = ref<InstanceType<typeof PhoneNumberInput> | null>(null)
const codeInputRef = ref<HTMLInputElement | null>(null)

// Modal instance
let modalInstance: Modal | null = null

// Component state
const showCodeInput = ref(false)
const phoneNumber = ref(props.initialPhoneNumber)
const verificationCode = ref('')
const isPhoneValid = ref(false)
const phoneError = ref('')
const codeError = ref('')
const loading = ref(false)
const loadingMessage = ref('')
const sendingCode = ref(false)
const verifyingCode = ref(false)
const countdown = ref(0)
let countdownInterval: NodeJS.Timeout | null = null

// Computed properties
const isCodeValid = computed(() => {
  return verificationCode.value.length === 6 && /^\d{6}$/.test(verificationCode.value)
})

const maskedPhoneNumber = computed(() => {
  if (!phoneNumber.value) return ''

  // Format for display - mask middle digits
  const cleaned = phoneNumber.value.replace(/\D/g, '')
  if (cleaned.length === 11 && cleaned.startsWith('1')) {
    const areaCode = cleaned.slice(1, 4)
    const middle = cleaned.slice(4, 7)
    const last = cleaned.slice(7, 11)
    return `+1 (${areaCode}) ***-${last}`
  } else if (cleaned.length === 10) {
    const areaCode = cleaned.slice(0, 3)
    const middle = cleaned.slice(3, 6)
    const last = cleaned.slice(6, 10)
    return `(${areaCode}) ***-${last}`
  }
  return phoneNumber.value
})

// Methods
function show() {
  if (modalInstance) {
    modalInstance.show()
  }
}

function hide() {
  if (modalInstance) {
    modalInstance.hide()
  }
}

function handleClose() {
  resetForm()
  emit('closed')
}

function resetForm() {
  showCodeInput.value = false
  verificationCode.value = ''
  phoneError.value = ''
  codeError.value = ''
  loading.value = false
  sendingCode.value = false
  verifyingCode.value = false
  stopCountdown()

  if (!props.initialPhoneNumber) {
    phoneNumber.value = ''
    isPhoneValid.value = false
  }
}

function handlePhoneValidation(isValid: boolean, formattedNumber: string) {
  isPhoneValid.value = isValid
  if (isValid && formattedNumber) {
    phoneNumber.value = formattedNumber
    phoneError.value = ''
  }
}

async function sendVerificationCode() {
  if (!isPhoneValid.value || !phoneNumber.value) {
    phoneError.value = 'Please enter a valid phone number'
    return
  }

  sendingCode.value = true
  phoneError.value = ''

  try {
    const response = await fetch('/api/auth/send-sms-code/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone_number: phoneNumber.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      showCodeInput.value = true
      startCountdown()
      emit('phone-sent', phoneNumber.value)

      // Focus the code input after transition
      nextTick(() => {
        codeInputRef.value?.focus()
      })

      await Swal.fire({
        icon: 'success',
        title: 'Code Sent!',
        text: `Verification code sent to ${maskedPhoneNumber.value}`,
        timer: 2000,
        showConfirmButton: false
      })
    } else {
      phoneError.value = data.error || 'Failed to send verification code'
    }
  } catch (error) {
    console.error('Error sending SMS code:', error)
    phoneError.value = 'Network error. Please try again.'
  } finally {
    sendingCode.value = false
  }
}

async function verifyCode() {
  if (!isCodeValid.value) {
    codeError.value = 'Please enter a valid 6-digit code'
    return
  }

  verifyingCode.value = true
  codeError.value = ''

  try {
    const response = await fetch('/api/auth/verify-sms-code/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone_number: phoneNumber.value,
        code: verificationCode.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      await Swal.fire({
        icon: 'success',
        title: 'Verified!',
        text: 'Phone number verified successfully',
        timer: 1500,
        showConfirmButton: false
      })

      emit('phone-verified', {
        phoneNumber: phoneNumber.value,
        verificationCode: verificationCode.value
      })

      hide()
    } else {
      codeError.value = data.error || 'Invalid verification code'
    }
  } catch (error) {
    console.error('Error verifying SMS code:', error)
    codeError.value = 'Network error. Please try again.'
  } finally {
    verifyingCode.value = false
  }
}

function resendCode() {
  sendVerificationCode()
}

function editPhoneNumber() {
  showCodeInput.value = false
  verificationCode.value = ''
  codeError.value = ''
  stopCountdown()

  nextTick(() => {
    phoneInputRef.value?.focus()
  })
}

function handleCodeInput() {
  codeError.value = ''

  // Auto-submit when 6 digits entered
  if (isCodeValid.value) {
    verifyCode()
  }
}

function handleCodeKeypress(event: KeyboardEvent) {
  // Only allow digits
  if (!/\d/.test(event.key) && !['Backspace', 'Delete', 'Tab', 'Enter'].includes(event.key)) {
    event.preventDefault()
  }

  // Submit on Enter
  if (event.key === 'Enter' && isCodeValid.value) {
    verifyCode()
  }
}

function startCountdown() {
  countdown.value = 30
  countdownInterval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      stopCountdown()
    }
  }, 1000)
}

function stopCountdown() {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
  countdown.value = 0
}

// Lifecycle
onMounted(() => {
  if (modalElement.value) {
    modalInstance = new Modal(modalElement.value, {
      backdrop: 'static',
      keyboard: true
    })

    modalElement.value.addEventListener('hidden.bs.modal', handleClose)

    if (props.autoShow) {
      show()
    }
  }
})

onUnmounted(() => {
  stopCountdown()
  if (modalInstance) {
    modalInstance.dispose()
  }
})

// Expose methods for parent components
defineExpose({
  show,
  hide,
  resetForm
})
</script>

<style scoped>
.letter-spacing-2 {
  letter-spacing: 0.5rem;
}

.text-sm {
  font-size: 0.875rem;
}

.modal-content {
  border-radius: 0.5rem;
}

.btn-link {
  font-size: 0.875rem;
}

/* Code input styling */
input[type="text"].text-center {
  padding: 1rem;
}

/* Animation for step transitions */
.modal-body > div {
  transition: opacity 0.3s ease-in-out;
}
</style>