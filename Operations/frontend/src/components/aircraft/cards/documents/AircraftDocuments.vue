<template>
  <div class="card">
    <!--begin::Card header-->
    <div class="card-header border-0 pt-5">
      <h3 class="card-title align-items-start flex-column">
        <span class="card-label fw-bold fs-3 mb-1">Aircraft Documents</span>
        <span class="text-muted mt-1 fw-semibold fs-7">Certificates, manuals, and other documentation</span>
      </h3>
      <div class="card-toolbar">
        <button class="btn btn-sm btn-light-primary">
          <KTIcon icon-name="document" icon-class="fs-3" />
          Upload Document
        </button>
      </div>
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body py-3">
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <!--begin::Document Categories-->
        <div class="mb-10">
          <!--begin::Certificates-->
          <div class="mb-8">
            <h5 class="fw-bold text-dark mb-4">Certificates & Registrations</h5>
            <div class="row">
              <div class="col-md-6 mb-4" v-for="cert in certificates" :key="cert.id">
                <div class="card card-custom h-100">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="symbol symbol-50px me-3">
                        <div class="symbol-label bg-light-success">
                          <KTIcon icon-name="document" icon-class="fs-2 text-success" />
                        </div>
                      </div>
                      <div class="flex-grow-1">
                        <div class="fw-bold text-dark fs-6 mb-1">{{ cert.name }}</div>
                        <div class="text-muted fs-7 mb-2">{{ cert.type }}</div>
                        <div class="d-flex align-items-center">
                          <span class="text-muted fs-8 me-3">Expires: {{ formatDate(cert.expiry) }}</span>
                          <span :class="`badge badge-light-${getExpiryColor(cert.expiry)} badge-sm`">
                            {{ getExpiryStatus(cert.expiry) }}
                          </span>
                        </div>
                      </div>
                      <div class="dropdown">
                        <button class="btn btn-icon btn-sm btn-light-primary" data-bs-toggle="dropdown">
                          <KTIcon icon-name="dots-vertical" icon-class="fs-3" />
                        </button>
                        <div class="dropdown-menu">
                          <a class="dropdown-item" href="#">Download</a>
                          <a class="dropdown-item" href="#">View</a>
                          <a class="dropdown-item" href="#">Update</a>
                          <div class="dropdown-divider"></div>
                          <a class="dropdown-item text-danger" href="#">Delete</a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Certificates-->

          <!--begin::Manuals & Documentation-->
          <div class="mb-8">
            <h5 class="fw-bold text-dark mb-4">Manuals & Documentation</h5>
            <div class="row">
              <div class="col-md-4 mb-4" v-for="manual in manuals" :key="manual.id">
                <div class="card card-custom h-100">
                  <div class="card-body p-4">
                    <div class="d-flex align-items-start">
                      <div class="symbol symbol-50px me-3">
                        <div class="symbol-label bg-light-info">
                          <KTIcon icon-name="book" icon-class="fs-2 text-info" />
                        </div>
                      </div>
                      <div class="flex-grow-1">
                        <div class="fw-bold text-dark fs-6 mb-1">{{ manual.name }}</div>
                        <div class="text-muted fs-7 mb-2">{{ manual.version }}</div>
                        <div class="text-muted fs-8">Updated: {{ formatDate(manual.updated) }}</div>
                      </div>
                      <div class="dropdown">
                        <button class="btn btn-icon btn-sm btn-light-primary" data-bs-toggle="dropdown">
                          <KTIcon icon-name="dots-vertical" icon-class="fs-3" />
                        </button>
                        <div class="dropdown-menu">
                          <a class="dropdown-item" href="#">Download</a>
                          <a class="dropdown-item" href="#">View</a>
                          <a class="dropdown-item" href="#">Update</a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Manuals & Documentation-->

          <!--begin::Other Documents-->
          <div class="mb-8">
            <h5 class="fw-bold text-dark mb-4">Other Documents</h5>
            
            <div v-if="otherDocuments && otherDocuments.length > 0">
              <!--begin::Table container-->
              <div class="table-responsive">
                <!--begin::Table-->
                <table class="table table-row-dashed table-row-gray-300 align-middle gs-0 gy-4">
                  <!--begin::Table head-->
                  <thead>
                    <tr class="fw-bold text-muted">
                      <th class="min-w-200px">Document Name</th>
                      <th class="min-w-100px">Type</th>
                      <th class="min-w-100px">Size</th>
                      <th class="min-w-120px">Uploaded</th>
                      <th class="min-w-100px text-end">Actions</th>
                    </tr>
                  </thead>
                  <!--end::Table head-->
                  <!--begin::Table body-->
                  <tbody>
                    <tr v-for="doc in otherDocuments" :key="doc.id">
                      <td>
                        <div class="d-flex align-items-center">
                          <div class="symbol symbol-40px me-3">
                            <div class="symbol-label bg-light-primary">
                              <KTIcon icon-name="document" icon-class="fs-3 text-primary" />
                            </div>
                          </div>
                          <div class="d-flex justify-content-start flex-column">
                            <a href="#" class="text-dark fw-bold text-hover-primary fs-6">
                              {{ doc.name }}
                            </a>
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="text-dark fw-bold fs-6">{{ doc.type }}</div>
                      </td>
                      <td>
                        <div class="text-dark fw-bold fs-6">{{ doc.size }}</div>
                      </td>
                      <td>
                        <div class="text-dark fw-bold fs-6">{{ formatDate(doc.uploaded) }}</div>
                      </td>
                      <td>
                        <div class="d-flex justify-content-end flex-shrink-0">
                          <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                            <KTIcon icon-name="arrow-down" icon-class="fs-3" />
                          </a>
                          <a href="#" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                            <KTIcon icon-name="eye" icon-class="fs-3" />
                          </a>
                          <a href="#" class="btn btn-icon btn-bg-light btn-active-color-danger btn-sm">
                            <KTIcon icon-name="trash" icon-class="fs-3" />
                          </a>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                  <!--end::Table body-->
                </table>
                <!--end::Table-->
              </div>
              <!--end::Table container-->
            </div>
            
            <div v-else class="text-center py-10">
              <div class="text-gray-400">No additional documents found</div>
              <button class="btn btn-primary mt-3">
                Upload Document
              </button>
            </div>
          </div>
          <!--end::Other Documents-->
        </div>
        <!--end::Document Categories-->
      </div>
    </div>
    <!--end::Card body-->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from "vue";
import ApiService from "@/core/services/ApiService";

export default defineComponent({
  name: "AircraftDocuments",
  props: {
    aircraft: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const certificates = ref<any[]>([]);
    const manuals = ref<any[]>([]);
    const otherDocuments = ref<any[]>([]);
    const documentsLoading = ref(false);

    const fetchDocuments = async () => {
      if (!props.aircraft?.id) return;
      
      try {
        documentsLoading.value = true;
        // This would be the actual API call when documents endpoint exists
        // const response = await ApiService.get(`/aircraft-documents/?aircraft=${props.aircraft.id}`);
        
        // For now, use mock data
        certificates.value = [
          {
            id: 1,
            name: 'Airworthiness Certificate',
            type: 'Certificate',
            expiry: '2024-12-31'
          },
          {
            id: 2,
            name: 'Registration Certificate',
            type: 'Certificate',
            expiry: '2025-06-15'
          },
          {
            id: 3,
            name: 'Radio Station License',
            type: 'License',
            expiry: '2024-03-20'
          }
        ];

        manuals.value = [
          {
            id: 1,
            name: 'Pilot Operating Handbook',
            version: 'Rev 5.2',
            updated: '2023-11-15'
          },
          {
            id: 2,
            name: 'Maintenance Manual',
            version: 'Ver 3.1',
            updated: '2023-10-20'
          },
          {
            id: 3,
            name: 'Emergency Procedures',
            version: 'Rev 2.0',
            updated: '2023-09-10'
          }
        ];

        otherDocuments.value = [
          {
            id: 1,
            name: 'Insurance Policy',
            type: 'PDF',
            size: '2.3 MB',
            uploaded: '2024-01-15'
          },
          {
            id: 2,
            name: 'Weight & Balance Report',
            type: 'PDF',
            size: '1.1 MB',
            uploaded: '2024-01-10'
          }
        ];
        
      } catch (error) {
        console.error("Error fetching documents:", error);
        certificates.value = [];
        manuals.value = [];
        otherDocuments.value = [];
      } finally {
        documentsLoading.value = false;
      }
    };

    const formatDate = (dateString?: string): string => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    };

    const getExpiryColor = (expiryDate?: string): string => {
      if (!expiryDate) return 'secondary';
      
      const expiry = new Date(expiryDate);
      const now = new Date();
      const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 3600 * 24));
      
      if (daysUntilExpiry < 0) return 'danger';
      if (daysUntilExpiry < 30) return 'warning';
      if (daysUntilExpiry < 90) return 'info';
      return 'success';
    };

    const getExpiryStatus = (expiryDate?: string): string => {
      if (!expiryDate) return 'Unknown';
      
      const expiry = new Date(expiryDate);
      const now = new Date();
      const daysUntilExpiry = Math.ceil((expiry.getTime() - now.getTime()) / (1000 * 3600 * 24));
      
      if (daysUntilExpiry < 0) return 'Expired';
      if (daysUntilExpiry < 30) return 'Expiring Soon';
      if (daysUntilExpiry < 90) return 'Valid';
      return 'Valid';
    };

    watch(() => props.aircraft, fetchDocuments, { immediate: true });

    return {
      certificates,
      manuals,
      otherDocuments,
      documentsLoading,
      formatDate,
      getExpiryColor,
      getExpiryStatus,
    };
  },
});
</script>