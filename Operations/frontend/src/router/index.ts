import {
  createRouter,
  createWebHistory,
  type RouteRecordRaw,
} from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useConfigStore } from "@/stores/config";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/dashboard",
    component: () => import("@/layouts/default-layout/DefaultLayout.vue"),
    meta: {
      middleware: "auth",
    },
    children: [
      {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("@/views/Dashboard.vue"),
        meta: {
          pageTitle: "Dashboard",
          breadcrumbs: ["Dashboards"],
        },
      },
      {
        path: "/builder",
        name: "builder",
        component: () => import("@/views/LayoutBuilder.vue"),
        meta: {
          pageTitle: "Layout Builder",
          breadcrumbs: ["Layout"],
        },
      },
      {
        path: "/crafted/pages/profile",
        name: "profile",
        component: () => import("@/components/page-layouts/Profile.vue"),
        meta: {
          breadcrumbs: ["Pages", "Profile"],
        },
        children: [
          {
            path: "overview",
            name: "profile-overview",
            component: () =>
              import("@/views/crafted/pages/profile/Overview.vue"),
            meta: {
              pageTitle: "Overview",
            },
          },
          {
            path: "projects",
            name: "profile-projects",
            component: () =>
              import("@/views/crafted/pages/profile/Projects.vue"),
            meta: {
              pageTitle: "Projects",
            },
          },
          {
            path: "campaigns",
            name: "profile-campaigns",
            component: () =>
              import("@/views/crafted/pages/profile/Campaigns.vue"),
            meta: {
              pageTitle: "Campaigns",
            },
          },
          {
            path: "documents",
            name: "profile-documents",
            component: () =>
              import("@/views/crafted/pages/profile/Documents.vue"),
            meta: {
              pageTitle: "Documents",
            },
          },
          {
            path: "connections",
            name: "profile-connections",
            component: () =>
              import("@/views/crafted/pages/profile/Connections.vue"),
            meta: {
              pageTitle: "Connections",
            },
          },
          {
            path: "activity",
            name: "profile-activity",
            component: () =>
              import("@/views/crafted/pages/profile/Activity.vue"),
            meta: {
              pageTitle: "Activity",
            },
          },
        ],
      },
      {
        path: "/crafted/pages/wizards/horizontal",
        name: "horizontal-wizard",
        component: () =>
          import("@/views/crafted/pages/wizards/HorizontalWizardPage.vue"),
        meta: {
          pageTitle: "Horizontal",
          breadcrumbs: ["Pages", "Wizard"],
        },
      },
      {
        path: "/crafted/pages/wizards/vertical",
        name: "vertical-wizard",
        component: () =>
          import("@/views/crafted/pages/wizards/VerticalWizardPage.vue"),
        meta: {
          pageTitle: "Vertical",
          breadcrumbs: ["Pages", "Wizard"],
        },
      },
      {
        path: "/crafted/account",
        name: "account",
        component: () => import("@/views/crafted/account/Account.vue"),
        meta: {
          breadcrumbs: ["Crafted", "Account"],
        },
        children: [
          {
            path: "overview",
            name: "account-overview",
            component: () => import("@/views/crafted/account/Overview.vue"),
            meta: {
              pageTitle: "Overview",
            },
          },
          {
            path: "settings",
            name: "account-settings",
            component: () => import("@/views/crafted/account/Settings.vue"),
            meta: {
              pageTitle: "Settings",
            },
          },
        ],
      },
      {
        path: "/apps/customers/getting-started",
        name: "apps-customers-getting-started",
        component: () => import("@/views/apps/customers/GettingStarted.vue"),
        meta: {
          pageTitle: "Getting Started",
          breadcrumbs: ["Apps", "Customers"],
        },
      },
      {
        path: "/apps/customers/customers-listing",
        name: "apps-customers-listing",
        component: () => import("@/views/apps/customers/CustomersListing.vue"),
        meta: {
          pageTitle: "Customers Listing",
          breadcrumbs: ["Apps", "Customers"],
        },
      },
      {
        path: "/apps/customers/customer-details",
        name: "apps-customers-details",
        component: () => import("@/views/apps/customers/CustomerDetails.vue"),
        meta: {
          pageTitle: "Customers Details",
          breadcrumbs: ["Apps", "Customers"],
        },
      },
      {
        path: "/apps/subscriptions/getting-started",
        name: "apps-subscriptions-getting-started",
        component: () =>
          import("@/views/apps/subscriptions/GettingStarted.vue"),
        meta: {
          pageTitle: "Getting Started",
          breadcrumbs: ["Apps", "Subscriptions"],
        },
      },
      {
        path: "/apps/subscriptions/subscription-list",
        name: "apps-subscriptions-subscription-list",
        component: () =>
          import("@/views/apps/subscriptions/SubscriptionList.vue"),
        meta: {
          pageTitle: "Getting Started",
          breadcrumbs: ["Apps", "Subscriptions"],
        },
      },
      {
        path: "/apps/subscriptions/add-subscription",
        name: "apps-subscriptions-add-subscription",
        component: () =>
          import("@/views/apps/subscriptions/AddSubscription.vue"),
        meta: {
          pageTitle: "Add Subscription",
          breadcrumbs: ["Apps", "Subscriptions"],
        },
      },
      {
        path: "/apps/subscriptions/view-subscription",
        name: "apps-subscriptions-view-subscription",
        component: () =>
          import("@/views/apps/subscriptions/ViewSubscription.vue"),
        meta: {
          pageTitle: "View Subscription",
          breadcrumbs: ["Apps", "Subscriptions"],
        },
      },
      {
        path: "/apps/calendar",
        name: "apps-calendar",
        component: () => import("@/views/apps/Calendar.vue"),
        meta: {
          pageTitle: "Calendar",
          breadcrumbs: ["Apps"],
        },
      },
      {
        path: "/apps/chat/private-chat",
        name: "apps-private-chat",
        component: () => import("@/views/apps/chat/Chat.vue"),
        meta: {
          pageTitle: "Private Chat",
          breadcrumbs: ["Apps", "Chat"],
        },
      },
      {
        path: "/apps/chat/group-chat",
        name: "apps-group-chat",
        component: () => import("@/views/apps/chat/Chat.vue"),
        meta: {
          pageTitle: "Group Chat",
          breadcrumbs: ["Apps", "Chat"],
        },
      },
      {
        path: "/apps/chat/drawer-chat",
        name: "apps-drawer-chat",
        component: () => import("@/views/apps/chat/DrawerChat.vue"),
        meta: {
          pageTitle: "Drawer Chat",
          breadcrumbs: ["Apps", "Chat"],
        },
      },
      {
        path: "/crafted/modals/general/invite-friends",
        name: "modals-general-invite-friends",
        component: () =>
          import("@/views/crafted/modals/general/InviteFriends.vue"),
        meta: {
          pageTitle: "Invite Friends",
          breadcrumbs: ["Crafted", "Modals", "General"],
        },
      },
      {
        path: "/crafted/modals/general/view-user",
        name: "modals-general-view-user",
        component: () => import("@/views/crafted/modals/general/ViewUsers.vue"),
        meta: {
          pageTitle: "View User",
          breadcrumbs: ["Crafted", "Modals", "General"],
        },
      },
      {
        path: "/crafted/modals/general/upgrade-plan",
        name: "modals-general-upgrade-plan",
        component: () =>
          import("@/views/crafted/modals/general/UpgradePlan.vue"),
        meta: {
          pageTitle: "Upgrade Plan",
          breadcrumbs: ["Crafted", "Modals", "General"],
        },
      },
      {
        path: "/crafted/modals/general/share-and-earn",
        name: "modals-general-share-and-earn",
        component: () =>
          import("@/views/crafted/modals/general/ShareAndEarn.vue"),
        meta: {
          pageTitle: "Share And Earn",
          breadcrumbs: ["Crafted", "Modals", "General"],
        },
      },
      {
        path: "/crafted/modals/forms/new-target",
        name: "modals-forms-new-target",
        component: () => import("@/views/crafted/modals/forms/NewTarget.vue"),
        meta: {
          pageTitle: "New Target",
          breadcrumbs: ["Crafted", "Modals", "Forms"],
        },
      },
      {
        path: "/crafted/modals/forms/new-card",
        name: "modals-forms-new-card",
        component: () => import("@/views/crafted/modals/forms/NewCard.vue"),
        meta: {
          pageTitle: "New Card",
          breadcrumbs: ["Crafted", "Modals", "Forms"],
        },
      },
      {
        path: "/crafted/modals/forms/new-address",
        name: "modals-forms-new-address",
        component: () => import("@/views/crafted/modals/forms/NewAddress.vue"),
        meta: {
          pageTitle: "New Address",
          breadcrumbs: ["Crafted", "Modals", "Forms"],
        },
      },
      {
        path: "/crafted/modals/forms/create-api-key",
        name: "modals-forms-create-api-key",
        component: () =>
          import("@/views/crafted/modals/forms/CreateApiKey.vue"),
        meta: {
          pageTitle: "Create Api Key",
          breadcrumbs: ["Crafted", "Modals", "Forms"],
        },
      },
      {
        path: "/crafted/modals/wizards/two-factor-auth",
        name: "modals-wizards-two-factor-auth",
        component: () =>
          import("@/views/crafted/modals/wizards/TwoFactorAuth.vue"),
        meta: {
          pageTitle: "Two Factory Auth",
          breadcrumbs: ["Crafted", "Modals", "Wizards"],
        },
      },
      {
        path: "/crafted/modals/wizards/create-app",
        name: "modals-wizards-create-app",
        component: () => import("@/views/crafted/modals/wizards/CreateApp.vue"),
        meta: {
          pageTitle: "Create App",
          breadcrumbs: ["Crafted", "Modals", "Wizards"],
        },
      },
      {
        path: "/crafted/modals/wizards/create-account",
        name: "modals-wizards-create-account",
        component: () =>
          import("@/views/crafted/modals/wizards/CreateAccount.vue"),
        meta: {
          pageTitle: "Create Account",
          breadcrumbs: ["Crafted", "Modals", "Wizards"],
        },
      },
      {
        path: "/crafted/widgets/lists",
        name: "widgets-list",
        component: () => import("@/views/crafted/widgets/Lists.vue"),
        meta: {
          pageTitle: "Lists",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/crafted/widgets/statistics",
        name: "widgets-statistics",
        component: () => import("@/views/crafted/widgets/Statistics.vue"),
        meta: {
          pageTitle: "Statistics",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/crafted/widgets/charts",
        name: "widgets-charts",
        component: () => import("@/views/crafted/widgets/Charts.vue"),
        meta: {
          pageTitle: "Charts",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/crafted/widgets/mixed",
        name: "widgets-mixed",
        component: () => import("@/views/crafted/widgets/Mixed.vue"),
        meta: {
          pageTitle: "Mixed",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/crafted/widgets/tables",
        name: "widgets-tables",
        component: () => import("@/views/crafted/widgets/Tables.vue"),
        meta: {
          pageTitle: "Tables",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/crafted/widgets/feeds",
        name: "widgets-feeds",
        component: () => import("@/views/crafted/widgets/Feeds.vue"),
        meta: {
          pageTitle: "Feeds",
          breadcrumbs: ["Crafted", "Widgets"],
        },
      },
      {
        path: "/account/settings",
        name: "user-account-settings", 
        component: () => import("@/views/account/Settings.vue"),
        meta: {
          pageTitle: "Account Settings",
          breadcrumbs: ["Account", "Settings"],
          middleware: "auth",
        },
      },
      // Administration Routes
      {
        path: "/admin/users",
        name: "admin-users",
        component: () => import("@/views/admin/Users.vue"),
        meta: {
          pageTitle: "Users",
          breadcrumbs: ["Administration", "Users"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/roles",
        name: "admin-roles",
        component: () => import("@/views/admin/Roles.vue"),
        meta: {
          pageTitle: "Roles",
          breadcrumbs: ["Administration", "Roles"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/departments",
        name: "admin-departments",
        component: () => import("@/views/admin/Departments.vue"),
        meta: {
          pageTitle: "Departments",
          breadcrumbs: ["Administration", "Departments"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/permissions",
        name: "admin-permissions",
        component: () => import("@/views/admin/Permissions.vue"),
        meta: {
          pageTitle: "Permissions",
          breadcrumbs: ["Administration", "Permissions"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/trips",
        name: "admin-trips",
        component: () => import("@/views/admin/Trips.vue"),
        meta: {
          pageTitle: "Trips",
          breadcrumbs: ["Administration", "Operations", "Trips"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/trips/:id",
        name: "admin-trip-view",
        component: () => import("@/views/admin/trips/ViewTrip.vue"),
        meta: {
          pageTitle: "Trip Details",
          breadcrumbs: ["Administration", "Operations", "Trips", "View"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/quotes",
        name: "admin-quotes",
        component: () => import("@/views/admin/Quotes.vue"),
        meta: {
          pageTitle: "Quotes",
          breadcrumbs: ["Administration", "Operations", "Quotes"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/quotes/:id",
        name: "admin-quote-view",
        component: () => import("@/views/admin/quotes/ViewQuote.vue"),
        meta: {
          pageTitle: "Quote Details",
          breadcrumbs: ["Administration", "Operations", "Quotes", "View"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/quotes/:id/edit",
        name: "admin-quote-edit",
        component: () => import("@/views/admin/quotes/EditQuote.vue"),
        meta: {
          pageTitle: "Edit Quote",
          breadcrumbs: ["Administration", "Operations", "Quotes", "Edit"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/patients",
        name: "admin-patients",
        component: () => import("@/views/admin/Patients.vue"),
        meta: {
          pageTitle: "Patients",
          breadcrumbs: ["Administration", "Operations", "Patients"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/passengers",
        name: "admin-passengers",
        component: () => import("@/views/admin/Passengers.vue"),
        meta: {
          pageTitle: "Passengers",
          breadcrumbs: ["Administration", "Operations", "Passengers"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/passengers/:id",
        name: "admin-passenger-details",
        component: () => import("@/views/admin/passengers/PassengerDetails.vue"),
        meta: {
          pageTitle: "Passenger Details",
          breadcrumbs: ["Administration", "Operations", "Passengers", "Details"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/contacts",
        name: "admin-contacts",
        component: () => import("@/views/admin/Contacts.vue"),
        meta: {
          pageTitle: "Contacts",
          breadcrumbs: ["Administration", "Contacts"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/contacts/:type/:id",
        name: "admin-contact-details",
        component: () => import("@/views/admin/contacts/ContactDetails.vue"),
        meta: {
          pageTitle: "Contact Details",
          breadcrumbs: ["Administration", "Contacts", "Details"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/staff",
        name: "admin-staff",
        component: () => import("@/views/admin/Staff.vue"),
        meta: {
          pageTitle: "Staff",
          breadcrumbs: ["Administration", "Contacts", "Staff"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/staff/:id",
        name: "admin-staff-detail",
        component: () => import("@/views/admin/StaffDetail.vue"),
        meta: {
          pageTitle: "Staff Details",
          breadcrumbs: ["Administration", "Contacts", "Staff", "Details"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/staff-roles",
        name: "admin-staff-roles",
        component: () => import("@/views/admin/StaffRoles.vue"),
        meta: {
          pageTitle: "Staff Roles",
          breadcrumbs: ["Administration", "System", "Staff Roles"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/fbos",
        name: "admin-fbos",
        component: () => import("@/views/admin/FBOs.vue"),
        meta: {
          pageTitle: "FBOs",
          breadcrumbs: ["Administration", "Contacts", "FBOs"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/fbos/:id",
        name: "admin-fbo-details",
        component: () => import("@/views/admin/fbos/FboDetails.vue"),
        meta: {
          pageTitle: "FBO Details",
          breadcrumbs: ["Administration", "Contacts", "FBOs", "Details"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/grounds",
        name: "admin-grounds",
        component: () => import("@/views/admin/Grounds.vue"),
        meta: {
          pageTitle: "Ground Transportation",
          breadcrumbs: ["Administration", "Contacts", "Ground"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/airports",
        name: "admin-airports",
        component: () => import("@/views/admin/Airports.vue"),
        meta: {
          pageTitle: "Airports",
          breadcrumbs: ["Administration", "Infrastructure", "Airports"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/aircraft",
        name: "admin-aircraft",
        component: () => import("@/views/admin/Aircraft.vue"),
        meta: {
          pageTitle: "Aircraft",
          breadcrumbs: ["Administration", "Infrastructure", "Aircraft"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/aircraft/:id",
        name: "admin-aircraft-details",
        component: () => import("@/views/admin/aircraft/AircraftDetails.vue"),
        meta: {
          pageTitle: "Aircraft Details",
          breadcrumbs: ["Administration", "Infrastructure", "Aircraft", "Details"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/transactions",
        name: "admin-transactions",
        component: () => import("@/views/admin/Transactions.vue"),
        meta: {
          pageTitle: "Transactions",
          breadcrumbs: ["Administration", "Financial", "Transactions"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/agreements",
        name: "admin-agreements",
        component: () => import("@/views/admin/Agreements.vue"),
        meta: {
          pageTitle: "Agreements",
          breadcrumbs: ["Administration", "Financial", "Agreements"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/documents",
        name: "admin-documents",
        component: () => import("@/views/admin/Documents.vue"),
        meta: {
          pageTitle: "Documents",
          breadcrumbs: ["Administration", "System", "Documents"],
          middleware: "auth",
        },
      },
      {
        path: "/admin/modifications",
        name: "admin-modifications",
        component: () => import("@/views/admin/Modifications.vue"),
        meta: {
          pageTitle: "Audit Log",
          breadcrumbs: ["Administration", "System", "Modifications"],
          middleware: "auth",
        },
      },
    ],
  },
  {
    path: "/",
    component: () => import("@/layouts/AuthLayout.vue"),
    children: [
      {
        path: "/sign-in",
        name: "sign-in",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/SignIn.vue"),
        meta: {
          pageTitle: "Sign In",
        },
      },
      {
        path: "/sign-up",
        name: "sign-up",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/SignUp.vue"),
        meta: {
          pageTitle: "Sign Up",
        },
      },
      {
        path: "/password-reset",
        name: "password-reset",
        component: () =>
          import("@/views/crafted/authentication/basic-flow/PasswordReset.vue"),
        meta: {
          pageTitle: "Password reset",
        },
      },
    ],
  },
  {
    path: "/",
    component: () => import("@/layouts/SystemLayout.vue"),
    children: [
      {
        // the 404 route, when none of the above matches
        path: "/404",
        name: "404",
        component: () => import("@/views/crafted/authentication/Error404.vue"),
        meta: {
          pageTitle: "Error 404",
        },
      },
      {
        path: "/500",
        name: "500",
        component: () => import("@/views/crafted/authentication/Error500.vue"),
        meta: {
          pageTitle: "Error 500",
        },
      },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/404",
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to) {
    // If the route has a hash, scroll to the section with the specified ID; otherwise, scroll toc the top of the page.
    if (to.hash) {
      return {
        el: to.hash,
        top: 80,
        behavior: "smooth",
      };
    } else {
      return {
        top: 0,
        left: 0,
        behavior: "smooth",
      };
    }
  },
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const configStore = useConfigStore();

  // current page view title
  document.title = `${to.meta.pageTitle} - ${import.meta.env.VITE_APP_NAME}`;

  // reset config to initial state
  configStore.resetLayoutConfig();

  // verify auth token before each page change
  authStore.verifyAuth();

  // before page access check if page requires authentication
  if (to.meta.middleware == "auth") {
    if (authStore.isAuthenticated) {
      next();
    } else {
      next({ name: "sign-in" });
    }
  } else {
    next();
  }
});

export default router;
