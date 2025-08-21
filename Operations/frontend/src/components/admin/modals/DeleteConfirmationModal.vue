<template>
  <div
    class="modal fade"
    :class="{ show: show }"
    :style="{ display: show ? 'block' : 'none' }"
    tabindex="-1"
    @click.self="$emit('close')"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="fw-bolder text-danger">Delete {{ itemType }}</h2>
          <div
            class="btn btn-icon btn-sm btn-active-icon-primary"
            @click="$emit('close')"
          >
            <i class="ki-duotone ki-cross fs-1">
              <span class="path1"></span>
              <span class="path2"></span>
            </i>
          </div>
        </div>

        <div class="modal-body">
          <div class="text-center">
            <i class="ki-duotone ki-trash fs-4x text-danger mb-4">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3"></span>
              <span class="path4"></span>
              <span class="path5"></span>
            </i>
            
            <h4 class="mb-3">Are you sure you want to delete this {{ itemType }}?</h4>
            
            <p class="text-gray-600 fs-5 mb-6" v-if="itemName">
              <strong>{{ itemName }}</strong> will be permanently deleted and cannot be recovered.
            </p>
            <p class="text-gray-600 fs-5 mb-6" v-else>
              This {{ itemType }} will be permanently deleted and cannot be recovered.
            </p>

            <div class="alert alert-light-danger d-flex align-items-center p-5 mb-6">
              <i class="ki-duotone ki-shield-tick fs-2hx text-danger me-4">
                <span class="path1"></span>
                <span class="path2"></span>
              </i>
              <div class="d-flex flex-column">
                <h5 class="mb-1">Warning</h5>
                <span>This action cannot be undone. Please proceed with caution.</span>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer flex-center">
          <button
            type="button"
            class="btn btn-light me-3"
            @click="$emit('close')"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-danger"
            :disabled="loading"
            @click="handleConfirm"
          >
            <span v-if="!loading" class="indicator-label">
              <i class="ki-duotone ki-trash fs-2 me-2">
                <span class="path1"></span>
                <span class="path2"></span>
                <span class="path3"></span>
                <span class="path4"></span>
                <span class="path5"></span>
              </i>
              Delete {{ itemType }}
            </span>
            <span v-else class="indicator-progress">
              Please wait...
              <span
                class="spinner-border spinner-border-sm align-middle ms-2"
              ></span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="show"
    class="modal-backdrop fade show"
  ></div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "delete-confirmation-modal",
  emits: ['close', 'confirm'],
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    itemName: {
      type: String,
      default: '',
    },
    itemType: {
      type: String,
      required: true,
    },
  },
  setup(props, { emit }) {
    const loading = ref(false);

    const handleConfirm = async () => {
      loading.value = true;
      try {
        emit('confirm');
      } finally {
        loading.value = false;
      }
    };

    return {
      loading,
      handleConfirm,
    };
  },
});
</script>