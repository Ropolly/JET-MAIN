<template>
  <!--begin::Toolbar-->
  <div id="kt_app_toolbar" class="app-toolbar py-3 py-lg-6">
    <!--begin::Toolbar container-->
    <div
      id="kt_app_toolbar_container"
      class="app-container d-flex flex-stack"
      :class="{
        'container-fluid': toolbarWidthFluid,
        'container-xxl': !toolbarWidthFluid,
      }"
    >
      <KTPageTitle />
      <!--begin::Actions-->
      <div class="d-flex align-items-center gap-2 gap-lg-3">
        <!-- Dynamic toolbar buttons based on current view -->
        <template v-for="action in toolbarActions" :key="action.id">
          <!-- Dropdown button -->
          <div v-if="action.isDropdown" class="dropdown">
            <button
              type="button"
              :class="getButtonClass(action.variant || 'secondary')"
              :id="action.id"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              :disabled="action.disabled"
            >
              <KTIcon v-if="action.icon" :icon-name="action.icon" icon-class="fs-2" />
              {{ action.label }}
              <KTIcon icon-name="down" icon-class="fs-5 ms-1" />
            </button>
            <ul class="dropdown-menu" :aria-labelledby="action.id">
              <template v-for="(item, index) in action.dropdownItems" :key="index">
                <li v-if="item.divider"><hr class="dropdown-divider"></li>
                <li v-else>
                  <a 
                    class="dropdown-item" 
                    :class="item.className"
                    href="#" 
                    @click.prevent="item.handler"
                  >
                    <KTIcon v-if="item.icon" :icon-name="item.icon" icon-class="fs-3 me-2" />
                    {{ item.label }}
                  </a>
                </li>
              </template>
            </ul>
          </div>
          <!-- Modal trigger button -->
          <a
            v-else-if="action.modalTarget"
            href="#"
            :class="getButtonClass(action.variant || 'primary')"
            data-bs-toggle="modal"
            :data-bs-target="action.modalTarget"
            :disabled="action.disabled"
          >
            <KTIcon v-if="action.icon" :icon-name="action.icon" icon-class="fs-2" />
            {{ action.label }}
          </a>
          <!-- Link button -->
          <a
            v-else-if="action.href"
            :href="action.href"
            :class="getButtonClass(action.variant || 'primary')"
            :disabled="action.disabled"
          >
            <KTIcon v-if="action.icon" :icon-name="action.icon" icon-class="fs-2" />
            {{ action.label }}
          </a>
          <!-- Click handler button -->
          <button
            v-else
            type="button"
            :class="getButtonClass(action.variant || 'primary')"
            @click="action.handler"
            :disabled="action.disabled"
          >
            <KTIcon v-if="action.icon" :icon-name="action.icon" icon-class="fs-2" />
            {{ action.label }}
          </button>
        </template>
      </div>
      <!--end::Actions-->
    </div>
    <!--end::Toolbar container-->
  </div>
  <!--end::Toolbar-->
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { toolbarWidthFluid } from "@/layouts/default-layout/config/helper";
import KTPageTitle from "@/layouts/default-layout/components/toolbar/PageTitle.vue";
import { useToolbarStore } from "@/stores/toolbar";

export default defineComponent({
  name: "layout-toolbar",
  components: {
    KTPageTitle,
  },
  setup() {
    const toolbarStore = useToolbarStore();
    
    const toolbarActions = computed(() => toolbarStore.actions);

    const getButtonClass = (variant: string) => {
      const baseClasses = "btn btn-sm fw-bold";
      switch (variant) {
        case 'primary':
          return `${baseClasses} btn-primary`;
        case 'secondary':
          return `${baseClasses} bg-body btn-color-gray-700 btn-active-color-primary`;
        case 'success':
          return `${baseClasses} btn-success`;
        case 'info':
          return `${baseClasses} btn-info`;
        case 'warning':
          return `${baseClasses} btn-warning`;
        case 'danger':
          return `${baseClasses} btn-danger`;
        case 'dark':
          return `${baseClasses} btn-dark`;
        default:
          return `${baseClasses} btn-primary`;
      }
    };

    return {
      toolbarWidthFluid,
      toolbarActions,
      getButtonClass,
    };
  },
});
</script>