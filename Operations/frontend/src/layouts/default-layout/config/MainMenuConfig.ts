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
    heading: "Operations",
    route: "/operations",
    pages: [
      {
        heading: "Trips",
        route: "/admin/trips",
        keenthemesIcon: "airplane",
        bootstrapIcon: "bi-airplane",
      },
      {
        heading: "Quotes",
        route: "/admin/quotes",
        keenthemesIcon: "document",
        bootstrapIcon: "bi-file-text",
      },
      {
        heading: "Patients",
        route: "/admin/patients",
        keenthemesIcon: "cross",
        bootstrapIcon: "bi-heart-pulse",
      },
      {
        heading: "Passengers",
        route: "/admin/passengers",
        keenthemesIcon: "people",
        bootstrapIcon: "bi-people",
      },
    ],
  },
  {
    heading: "Contacts",
    route: "/contacts",
    pages: [
      {
        heading: "Contacts",
        route: "/admin/contacts",
        keenthemesIcon: "address-book",
        bootstrapIcon: "bi-person-lines-fill",
      },
      {
        heading: "FBOs",
        route: "/admin/fbos",
        keenthemesIcon: "home",
        bootstrapIcon: "bi-building",
      },
      {
        heading: "Ground Transportation",
        route: "/admin/grounds",
        keenthemesIcon: "truck",
        bootstrapIcon: "bi-truck",
      },
      {
        heading: "Staff",
        route: "/admin/staff",
        keenthemesIcon: "people",
        bootstrapIcon: "bi-people-fill",
      },
    ],
  },
  {
    heading: "Infrastructure",
    route: "/infrastructure",
    pages: [
      {
        heading: "Airports",
        route: "/admin/airports",
        keenthemesIcon: "geolocation",
        bootstrapIcon: "bi-geo-alt",
      },
      {
        heading: "Aircraft",
        route: "/admin/aircraft",
        keenthemesIcon: "airplane",
        bootstrapIcon: "bi-airplane-engines",
      },
    ],
  },
  {
    heading: "Administration Menu",
    route: "/admin",
    pages: [
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
          {
            heading: "Staff Roles",
            route: "/admin/staff-roles",
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
        heading: "calendarApp",
        route: "/apps/calendar",
        keenthemesIcon: "calendar-8",
        bootstrapIcon: "bi-calendar3-event",
      },
    ],
  },
];

export default MainMenuConfig;
