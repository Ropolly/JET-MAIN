<template>
  <div class="mb-4">
    <label :for="inputId" class="form-label fw-semibold fs-6" :class="{ 'required': required }">
      {{ label }}
    </label>
    <div class="position-relative">
      <input
        :id="inputId"
        ref="phoneInput"
        type="tel"
        :class="inputClasses"
        :placeholder="placeholder"
        :value="formattedPhoneNumber"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        :readonly="readonly"
        :disabled="disabled"
        autocomplete="tel"
      />
      <div v-if="validationState === 'invalid'" class="invalid-feedback">
        {{ errorMessage }}
      </div>
      <div v-if="validationState === 'valid'" class="valid-feedback">
        Valid phone number
      </div>
    </div>
    <div v-if="helpText" class="form-text text-muted">
      {{ helpText }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'

interface Props {
  modelValue: string
  label?: string
  placeholder?: string
  required?: boolean
  readonly?: boolean
  disabled?: boolean
  helpText?: string
  validateOnInput?: boolean
  autoFormat?: boolean
  id?: string
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'validation-change', isValid: boolean, formattedNumber: string): void
  (e: 'focus'): void
  (e: 'blur'): void
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Phone Number',
  placeholder: '(555) 123-4567',
  required: false,
  readonly: false,
  disabled: false,
  helpText: '',
  validateOnInput: true,
  autoFormat: true,
  id: undefined
})

const emit = defineEmits<Emits>()

const phoneInput = ref<HTMLInputElement | null>(null)
const isFocused = ref(false)
const validationState = ref<'valid' | 'invalid' | 'neutral'>('neutral')
const errorMessage = ref('')

const inputId = computed(() => props.id || `phone-input-${Math.random().toString(36).substr(2, 9)}`)

const formattedPhoneNumber = ref('')

// Initialize formatted number
watch(() => props.modelValue, (newValue) => {
  if (props.autoFormat) {
    // modelValue should be digits only, format for display
    formattedPhoneNumber.value = formatPhoneNumber(newValue)
  } else {
    formattedPhoneNumber.value = newValue
  }
  if (props.validateOnInput) {
    validatePhoneNumber()
  }
}, { immediate: true })

const inputClasses = computed(() => {
  const baseClasses = ['form-control', 'form-control-solid']

  if (validationState.value === 'valid') {
    baseClasses.push('is-valid')
  } else if (validationState.value === 'invalid') {
    baseClasses.push('is-invalid')
  }

  if (isFocused.value) {
    baseClasses.push('focused')
  }

  return baseClasses.join(' ')
})

function formatPhoneNumber(value: string): string {
  if (!value) return ''

  // Remove all non-digit characters
  const digitsOnly = value.replace(/\D/g, '')

  // Handle different lengths for US format
  if (digitsOnly.length === 0) {
    return ''
  } else if (digitsOnly.length <= 3) {
    return `(${digitsOnly}`
  } else if (digitsOnly.length <= 6) {
    return `(${digitsOnly.slice(0, 3)}) ${digitsOnly.slice(3)}`
  } else if (digitsOnly.length <= 10) {
    return `(${digitsOnly.slice(0, 3)}) ${digitsOnly.slice(3, 6)}-${digitsOnly.slice(6)}`
  } else {
    // For 11+ digits, assume it's a complete US number and format accordingly
    return `(${digitsOnly.slice(0, 3)}) ${digitsOnly.slice(3, 6)}-${digitsOnly.slice(6, 10)}`
  }
}

function toE164Format(phoneNumber: string): string {
  const digitsOnly = phoneNumber.replace(/\D/g, '')

  if (digitsOnly.length === 10) {
    return `+1${digitsOnly}`
  } else if (digitsOnly.length === 11 && digitsOnly.startsWith('1')) {
    return `+${digitsOnly}`
  } else if (phoneNumber.startsWith('+')) {
    return `+${digitsOnly}`
  } else {
    return `+1${digitsOnly}`
  }
}

function validatePhoneNumber(): boolean {
  // Use the raw modelValue (digits only) for validation instead of formatted display
  const rawValue = props.modelValue

  if (!rawValue) {
    if (props.required) {
      validationState.value = 'invalid'
      errorMessage.value = 'Phone number is required'
      emit('validation-change', false, '')
      return false
    } else {
      validationState.value = 'neutral'
      errorMessage.value = ''
      emit('validation-change', true, '')
      return true
    }
  }

  const digitsOnly = rawValue.replace(/\D/g, '')

  // Basic validation for US numbers
  if (digitsOnly.length === 10 || (digitsOnly.length === 11 && digitsOnly.startsWith('1'))) {
    validationState.value = 'valid'
    errorMessage.value = ''
    const e164Number = toE164Format(digitsOnly)
    emit('validation-change', true, e164Number)
    return true
  } else if (digitsOnly.length >= 10 && digitsOnly.length <= 15) {
    // International number validation
    validationState.value = 'valid'
    errorMessage.value = ''
    const e164Number = toE164Format(digitsOnly)
    emit('validation-change', true, e164Number)
    return true
  } else {
    validationState.value = 'invalid'
    errorMessage.value = 'Please enter a valid phone number'
    emit('validation-change', false, '')
    return false
  }
}

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  let value = target.value

  if (props.autoFormat) {
    const cursorPosition = target.selectionStart || 0
    const prevLength = formattedPhoneNumber.value.length

    formattedPhoneNumber.value = formatPhoneNumber(value)

    // Adjust cursor position after formatting
    nextTick(() => {
      if (phoneInput.value) {
        const newLength = formattedPhoneNumber.value.length
        const lengthDifference = newLength - prevLength
        const newCursorPosition = Math.max(0, cursorPosition + lengthDifference)
        phoneInput.value.setSelectionRange(newCursorPosition, newCursorPosition)
      }
    })
  } else {
    formattedPhoneNumber.value = value
  }

  // Emit the digits only - let validation determine if it's valid for E.164
  const digitsOnly = value.replace(/\D/g, '')
  emit('update:modelValue', digitsOnly)

  if (props.validateOnInput) {
    validatePhoneNumber()
  }
}

function handleBlur() {
  isFocused.value = false
  validatePhoneNumber()
  emit('blur')
}

function handleFocus() {
  isFocused.value = true
  emit('focus')
}

// Expose validation method for parent components
defineExpose({
  validate: validatePhoneNumber,
  focus: () => phoneInput.value?.focus()
})
</script>

<style scoped>
.form-control.focused {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-label.required::after {
  content: "*";
  color: #dc3545;
  margin-left: 4px;
}
</style>