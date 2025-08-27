# Pagination Implementation Guide for Admin Pages

## Overview
All admin CRUD pages need to be updated to support server-side pagination following the Airports.vue pattern.

## Backend Changes (COMPLETED)
- ✅ Created StandardPagination class in api/views.py
- ✅ Applied pagination to BaseViewSet (all ViewSets inherit this)
- ✅ Page size: 25 (default), max: 100

## Frontend Changes Required

### 1. Add Pagination State Variables
Add these after existing refs in setup():
```typescript
const totalItems = ref(0);
const currentPage = ref(1);
const pageSize = ref(25);
const searchTimeout = ref<NodeJS.Timeout | null>(null);
```

### 2. Update KTDatatable Component Props
Add these props to the KTDatatable component:
```vue
@page-change="onPageChange"
:total="totalItems"
:current-page="currentPage"
:items-per-page="pageSize"
```

### 3. Update Fetch Method
Replace existing fetch method with pagination support:
```typescript
const fetchData = async (page: number = 1, pageLimit: number = 25, searchQuery: string = '', statusFilter: string = 'all') => {
  try {
    loading.value = true;
    error.value = null;
    
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('page_size', pageLimit.toString());
    if (searchQuery.trim()) {
      params.append('search', searchQuery.trim());
    }
    // Add status filter if applicable
    if (statusFilter !== 'all') {
      params.append('status', statusFilter);
    }
    
    const { data } = await ApiService.get(`/endpoint/?${params}`);
    items.value = data.results || [];
    totalItems.value = data.count || 0;
    currentPage.value = page;
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to fetch data";
    items.value = [];
    totalItems.value = 0;
  } finally {
    loading.value = false;
    setTimeout(() => {
      MenuComponent.reinitialization();
    }, 100);
  }
};
```

### 4. Update Search Method with Debouncing
Replace searchItems method:
```typescript
const searchItems = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  
  searchTimeout.value = setTimeout(async () => {
    currentPage.value = 1;
    await fetchData(1, pageSize.value, search.value);
    MenuComponent.reinitialization();
  }, 500);
};
```

### 5. Add Pagination Event Handlers
Add these new methods:
```typescript
const onPageChange = async (page: number) => {
  await fetchData(page, pageSize.value, search.value);
  MenuComponent.reinitialization();
};

const onItemsPerPageChange = async (newPageSize: number) => {
  pageSize.value = newPageSize;
  currentPage.value = 1;
  await fetchData(1, newPageSize, search.value);
  setTimeout(() => {
    MenuComponent.reinitialization();
  }, 0);
};
```

### 6. Update onMounted
```typescript
onMounted(async () => {
  await fetchData(1, pageSize.value, '');
  // ... rest of onMounted code
});
```

### 7. Update Return Statement
Add new properties to return statement:
```typescript
totalItems,
currentPage,
pageSize,
onPageChange,
```

### 8. Update Delete/Refresh Calls
Replace all `fetchData()` calls with:
```typescript
fetchData(currentPage.value, pageSize.value, search.value)
```

### 9. Clean Up onUnmounted
Add cleanup for search timeout:
```typescript
onUnmounted(() => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }
  // ... rest of cleanup
});
```

## Pages Status

### Completed ✅
- Airports.vue (template)
- Trips.vue
- Backend all ViewSets

### To Update
- [ ] Quotes.vue (has tabs like Trips)
- [ ] Patients.vue
- [ ] Passengers.vue
- [ ] Contacts.vue
- [ ] Fbos.vue
- [ ] Grounds.vue (Ground Transportation)
- [ ] Staff.vue
- [ ] Aircraft.vue
- [ ] Users.vue
- [ ] Roles.vue
- [ ] Departments.vue (if exists)
- [ ] Permissions.vue (if exists)
- [ ] Transactions.vue (if exists)
- [ ] Agreements.vue (if exists)
- [ ] Documents.vue (if exists)
- [ ] Modifications.vue (if exists)
- [ ] StaffRoles.vue

## Special Considerations

### Pages with Tabs (Quotes, Trips)
- Store status counts separately
- Pass status filter to fetch method
- Reset to page 1 when changing tabs
- Update handleTabChange method:
```typescript
const handleTabChange = async (tab: string) => {
  activeTab.value = tab;
  currentPage.value = 1;
  await fetchData(1, pageSize.value, search.value, tab);
};
```

### Pages with Complex Filters
- Add filter parameters to fetchData method
- Include filters in URLSearchParams
- Reset to page 1 when filters change

### Search Fields by Entity
Configure backend search_fields in ViewSets:
- Quotes: contact__first_name, contact__last_name, status
- Patients: info__first_name, info__last_name, status
- Contacts: first_name, last_name, business_name, email
- Aircraft: tail_number, make, model
- Users: first_name, last_name, email
- Etc.

## Testing Checklist
- [ ] Search works with debouncing
- [ ] Page navigation works
- [ ] Items per page change works
- [ ] Delete actions refresh current page
- [ ] Create actions reset to page 1
- [ ] Tab changes (if applicable) reset to page 1
- [ ] Total count displays correctly
- [ ] Loading states work properly

## Common Issues & Fixes

1. **initData.value not defined**: Remove all references to initData, not needed with server-side pagination
2. **searchingFunc not needed**: Remove this function, search is handled server-side
3. **Menu not reinitializing**: Ensure MenuComponent.reinitialization() is called after data updates
4. **Tabs not filtering**: Pass status parameter to API call in fetchData