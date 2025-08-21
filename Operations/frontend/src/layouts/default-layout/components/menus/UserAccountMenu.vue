<template>
  <!--begin::Menu-->
  <div
    class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold py-4 fs-6 w-275px"
    data-kt-menu="true"
  >
    <!--begin::Menu item-->
    <div class="menu-item px-3">
      <div class="menu-content d-flex align-items-center px-3">
        <!--begin::Avatar-->
        <div class="symbol symbol-50px me-5">
          <div class="symbol-label bg-light-primary">
            <span class="text-primary fw-bold fs-4">
              {{ getUserInitials() }}
            </span>
          </div>
        </div>
        <!--end::Avatar-->

        <!--begin::Username-->
        <div class="d-flex flex-column">
          <div class="fw-bold d-flex align-items-center fs-5">
            {{ getUserName() }}
          </div>
          <a href="#" class="fw-semibold text-muted text-hover-primary fs-7">
            {{ getUserEmail() }}
          </a>
        </div>
        <!--end::Username-->
      </div>
    </div>
    <!--end::Menu item-->

    <!--begin::Menu separator-->
    <div class="separator my-2"></div>
    <!--end::Menu separator-->

    <!--begin::Menu item-->
    <div class="menu-item px-5 my-1">
      <router-link to="/account/settings" class="menu-link px-5">
        Account Settings
      </router-link>
    </div>
    <!--end::Menu item-->

    <!--begin::Menu item-->
    <div class="menu-item px-5">
      <a @click="signOut()" class="menu-link px-5"> Sign Out </a>
    </div>
    <!--end::Menu item-->
  </div>
  <!--end::Menu-->
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { computed, defineComponent } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "kt-user-menu",
  components: {},
  setup() {
    const router = useRouter();
    const store = useAuthStore();

    const signOut = () => {
      store.logout();
      router.push({ name: "sign-in" });
    };

    const getUserInitials = (): string => {
      if (store.user) {
        const first = store.user.first_name?.charAt(0) || '';
        const last = store.user.last_name?.charAt(0) || '';
        return (first + last).toUpperCase() || store.user.email?.charAt(0).toUpperCase() || 'U';
      }
      return 'U';
    };

    const getUserName = (): string => {
      if (store.user) {
        if (store.user.first_name || store.user.last_name) {
          return `${store.user.first_name || ''} ${store.user.last_name || ''}`.trim();
        }
        return store.user.username || store.user.email || 'User';
      }
      return 'User';
    };

    const getUserEmail = (): string => {
      return store.user?.email || 'user@jetmed.com';
    };

    return {
      signOut,
      getUserInitials,
      getUserName,
      getUserEmail,
      getAssetPath,
    };
  },
});
</script>