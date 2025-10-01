<template>
  <!--begin::Navbar-->
  <div class="app-navbar flex-shrink-0 ms-auto">
    <!--begin::Search-->
    <div class="app-navbar-item align-items-stretch ms-1 ms-md-4">
      <KTSearch />
    </div>
    <!--end::Search-->
    <!--begin::Theme mode-->
    <div class="app-navbar-item ms-1 ms-md-3">
      <!--begin::Menu toggle-->
      <a
        href="#"
        class="btn btn-icon btn-custom btn-icon-muted btn-active-light btn-active-color-primary w-30px h-30px w-md-40px h-md-40px"
        data-kt-menu-trigger="{default:'click', lg: 'hover'}"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
      >
        <KTIcon
          v-if="themeMode === 'light'"
          icon-name="night-day"
          icon-class="fs-2"
        />
        <KTIcon v-else icon-name="moon" icon-class="fs-2" />
      </a>
      <!--begin::Menu toggle-->
      <KTThemeModeSwitcher />
    </div>
    <!--end::Theme mode-->
    <!--begin::User menu-->
    <div class="app-navbar-item ms-1 ms-md-4" id="kt_header_user_menu_toggle">
      <!--begin::Menu wrapper-->
      <div
        class="cursor-pointer symbol symbol-35px"
        data-kt-menu-trigger="{default: 'click', lg: 'hover'}"
        data-kt-menu-attach="parent"
        data-kt-menu-placement="bottom-end"
      >
        <div class="symbol-label bg-light-primary">
          <span class="text-primary fw-bold fs-6">
            {{ getUserInitials() }}
          </span>
        </div>
      </div>
      <KTUserMenu />
      <!--end::Menu wrapper-->
    </div>
    <!--end::User menu-->
    <!--begin::Header menu toggle-->
    <div class="app-navbar-item d-lg-none ms-2 me-n2">
      <div
        class="btn btn-flex btn-icon btn-active-color-primary w-30px h-30px"
        id="kt_app_header_menu_toggle"
      >
        <KTIcon icon-name="element-4" icon-class="fs-2" />
      </div>
    </div>
    <!--end::Header menu toggle-->
  </div>
  <!--end::Navbar-->
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { computed, defineComponent } from "vue";
import KTSearch from "@/layouts/default-layout/components/search/Search.vue";
import KTUserMenu from "@/layouts/default-layout/components/menus/UserAccountMenu.vue";
import KTThemeModeSwitcher from "@/layouts/default-layout/components/theme-mode/ThemeModeSwitcher.vue";
import { ThemeModeComponent } from "@/assets/ts/layout";
import { useThemeStore } from "@/stores/theme";
import { useAuthStore } from "@/stores/auth";

export default defineComponent({
  name: "header-navbar",
  components: {
    KTSearch,
    KTUserMenu,
    KTThemeModeSwitcher,
  },
  setup() {
    const store = useThemeStore();
    const authStore = useAuthStore();

    const themeMode = computed(() => {
      if (store.mode === "system") {
        return ThemeModeComponent.getSystemMode();
      }
      return store.mode;
    });

    const getUserInitials = (): string => {
      if (authStore.user) {
        const first = authStore.user.first_name?.charAt(0) || '';
        const last = authStore.user.last_name?.charAt(0) || '';
        return (first + last).toUpperCase() || authStore.user.email?.charAt(0).toUpperCase() || 'U';
      }
      return 'U';
    };

    return {
      themeMode,
      getAssetPath,
      getUserInitials,
    };
  },
});
</script>
