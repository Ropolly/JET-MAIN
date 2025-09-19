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
        heading: "Trips",
        route: "/admin/trips",
        keenthemesIcon: "airplane",
        bootstrapIcon: "bi-airplane",
      },
      {
        heading: "PAX",
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
          {
            heading: "Staff Roles",
            route: "/admin/staff-roles",
          },
        ],
      },
    ],
  },
];

export default MainMenuConfig;
