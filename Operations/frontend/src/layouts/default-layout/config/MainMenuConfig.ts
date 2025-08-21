import type { MenuItem } from "@/layouts/default-layout/config/types";

const MainMenuConfig: Array<MenuItem> = [
  {
    pages: [
      {
        heading: "dashboard",
        route: "/dashboard",
        keenthemesIcon: "element-11",
        bootstrapIcon: "bi-app-indicator",
      },
    ],
  },
  {
    heading: "craft",
    route: "/crafted",
    pages: [
      {
        sectionTitle: "pages",
        route: "/pages",
        keenthemesIcon: "element-plus",
        bootstrapIcon: "bi-archive",
        sub: [
          {
            sectionTitle: "profile",
            route: "/profile",
            sub: [
              {
                heading: "profileOverview",
                route: "/crafted/pages/profile/overview",
              },
              {
                heading: "projects",
                route: "/crafted/pages/profile/projects",
              },
              {
                heading: "campaigns",
                route: "/crafted/pages/profile/campaigns",
              },
              {
                heading: "documents",
                route: "/crafted/pages/profile/documents",
              },
              {
                heading: "connections",
                route: "/crafted/pages/profile/connections",
              },
              {
                heading: "activity",
                route: "/crafted/pages/profile/activity",
              },
            ],
          },
          {
            sectionTitle: "wizards",
            route: "/wizard",
            sub: [
              {
                heading: "horizontal",
                route: "/crafted/pages/wizards/horizontal",
              },
              {
                heading: "vertical",
                route: "/crafted/pages/wizards/vertical",
              },
            ],
          },
        ],
      },
      {
        sectionTitle: "account",
        route: "/account",
        keenthemesIcon: "profile-circle",
        bootstrapIcon: "bi-person",
        sub: [
          {
            heading: "accountOverview",
            route: "/crafted/account/overview",
          },
          {
            heading: "settings",
            route: "/crafted/account/settings",
          },
        ],
      },
      {
        sectionTitle: "authentication",
        keenthemesIcon: "fingerprint-scanning",
        bootstrapIcon: "bi-sticky",
        sub: [
          {
            sectionTitle: "basicFlow",
            sub: [
              {
                heading: "signIn",
                route: "/sign-in",
              },
              {
                heading: "signUp",
                route: "/sign-up",
              },
              {
                heading: "passwordReset",
                route: "/password-reset",
              },
            ],
          },
          {
            heading: "multiStepSignUp",
            route: "/multi-step-sign-up",
          },
          {
            heading: "error404",
            route: "/404",
          },
          {
            heading: "error500",
            route: "/500",
          },
        ],
      },
      {
        sectionTitle: "modals",
        route: "/modals",
        keenthemesIcon: "design",
        bootstrapIcon: "bi-shield-check",
        sub: [
          {
            sectionTitle: "general",
            route: "/general",
            sub: [
              {
                heading: "inviteFriends",
                route: "/crafted/modals/general/invite-friends",
              },
              {
                heading: "viewUsers",
                route: "/crafted/modals/general/view-user",
              },
              {
                heading: "upgradePlan",
                route: "/crafted/modals/general/upgrade-plan",
              },
              {
                heading: "shareAndEarn",
                route: "/crafted/modals/general/share-and-earn",
              },
            ],
          },
          {
            sectionTitle: "forms",
            route: "/forms",
            sub: [
              {
                heading: "newTarget",
                route: "/crafted/modals/forms/new-target",
              },
              {
                heading: "newCard",
                route: "/crafted/modals/forms/new-card",
              },
              {
                heading: "newAddress",
                route: "/crafted/modals/forms/new-address",
              },
              {
                heading: "createAPIKey",
                route: "/crafted/modals/forms/create-api-key",
              },
            ],
          },
          {
            sectionTitle: "wizards",
            route: "/wizards",
            sub: [
              {
                heading: "twoFactorAuth",
                route: "/crafted/modals/wizards/two-factor-auth",
              },
              {
                heading: "createApp",
                route: "/crafted/modals/wizards/create-app",
              },
              {
                heading: "createAccount",
                route: "/crafted/modals/wizards/create-account",
              },
            ],
          },
        ],
      },
      {
        sectionTitle: "widgets",
        route: "/widgets",
        keenthemesIcon: "element-7",
        bootstrapIcon: "bi-layers",
        sub: [
          {
            heading: "widgetsLists",
            route: "/crafted/widgets/lists",
          },
          {
            heading: "widgetsStatistics",
            route: "/crafted/widgets/statistics",
          },
          {
            heading: "widgetsCharts",
            route: "/crafted/widgets/charts",
          },
          {
            heading: "widgetsMixed",
            route: "/crafted/widgets/mixed",
          },
          {
            heading: "widgetsTables",
            route: "/crafted/widgets/tables",
          },
          {
            heading: "widgetsFeeds",
            route: "/crafted/widgets/feeds",
          },
        ],
      },
    ],
  },
  {
    heading: "administration",
    route: "/admin",
    pages: [
      {
        sectionTitle: "Operations",
        route: "/operations",
        keenthemesIcon: "airplane",
        bootstrapIcon: "bi-airplane",
        sub: [
          {
            heading: "Trips",
            route: "/admin/trips",
          },
          {
            heading: "Quotes",
            route: "/admin/quotes",
          },
          {
            heading: "Patients",
            route: "/admin/patients",
          },
          {
            heading: "Passengers",
            route: "/admin/passengers",
          },
        ],
      },
      {
        sectionTitle: "Contacts",
        route: "/contacts",
        keenthemesIcon: "address-book",
        bootstrapIcon: "bi-people",
        sub: [
          {
            heading: "Contacts",
            route: "/admin/contacts",
          },
          {
            heading: "FBOs",
            route: "/admin/fbos",
          },
          {
            heading: "Ground Transportation",
            route: "/admin/grounds",
          },
        ],
      },
      {
        sectionTitle: "Infrastructure",
        route: "/infrastructure",
        keenthemesIcon: "geolocation",
        bootstrapIcon: "bi-geo-alt",
        sub: [
          {
            heading: "Airports",
            route: "/admin/airports",
          },
          {
            heading: "Aircraft",
            route: "/admin/aircraft",
          },
        ],
      },
      {
        sectionTitle: "Administration",
        route: "/administration",
        keenthemesIcon: "security-user",
        bootstrapIcon: "bi-shield-lock",
        sub: [
          {
            heading: "Users",
            route: "/admin/users",
          },
          {
            heading: "Roles",
            route: "/admin/roles",
          },
          {
            heading: "Departments",
            route: "/admin/departments",
          },
          {
            heading: "Permissions",
            route: "/admin/permissions",
          },
        ],
      },
      {
        sectionTitle: "Financial",
        route: "/financial",
        keenthemesIcon: "dollar",
        bootstrapIcon: "bi-currency-dollar",
        sub: [
          {
            heading: "Transactions",
            route: "/admin/transactions",
          },
          {
            heading: "Agreements",
            route: "/admin/agreements",
          },
        ],
      },
      {
        sectionTitle: "System",
        route: "/system",
        keenthemesIcon: "setting-2",
        bootstrapIcon: "bi-gear",
        sub: [
          {
            heading: "Documents",
            route: "/admin/documents",
          },
          {
            heading: "Modifications",
            route: "/admin/modifications",
          },
        ],
      },
    ],
  },
  {
    heading: "apps",
    route: "/apps",
    pages: [
      {
        sectionTitle: "customers",
        route: "/customers",
        keenthemesIcon: "abstract-38",
        bootstrapIcon: "bi-printer",
        sub: [
          {
            heading: "gettingStarted",
            route: "/apps/customers/getting-started",
          },
          {
            heading: "customersListing",
            route: "/apps/customers/customers-listing",
          },
          {
            heading: "customerDetails",
            route: "/apps/customers/customer-details",
          },
        ],
      },
      {
        sectionTitle: "subscriptions",
        route: "/subscriptions",
        keenthemesIcon: "basket",
        bootstrapIcon: "bi-cart",
        sub: [
          {
            heading: "getStarted",
            route: "/apps/subscriptions/getting-started",
          },
          {
            heading: "subscriptionList",
            route: "/apps/subscriptions/subscription-list",
          },
          {
            heading: "addSubscription",
            route: "/apps/subscriptions/add-subscription",
          },
          {
            heading: "viewSubscription",
            route: "/apps/subscriptions/view-subscription",
          },
        ],
      },
      {
        heading: "calendarApp",
        route: "/apps/calendar",
        keenthemesIcon: "calendar-8",
        bootstrapIcon: "bi-calendar3-event",
      },
      {
        sectionTitle: "chat",
        route: "/chat",
        keenthemesIcon: "message-text-2",
        bootstrapIcon: "bi-chat-left",
        sub: [
          {
            heading: "privateChat",
            route: "/apps/chat/private-chat",
          },
          {
            heading: "groupChat",
            route: "/apps/chat/group-chat",
          },
          {
            heading: "drawerChat",
            route: "/apps/chat/drawer-chat",
          },
        ],
      },
    ],
  },
];

export default MainMenuConfig;
