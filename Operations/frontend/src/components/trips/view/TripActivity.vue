<template>
  <!--begin::Activity Card-->
  <div class="card card-flush">
    <!--begin::Card header-->
    <div class="card-header">
      <!--begin::Card title-->
      <div class="card-title">
        <h2 class="fw-bold">Trip Activity</h2>
      </div>
      <!--end::Card title-->

      <!--begin::Card toolbar-->
      <div class="card-toolbar">
        <button class="btn btn-light-primary btn-sm me-3" @click="showAddComment = !showAddComment">
          <KTIcon icon-name="plus" icon-class="fs-6" />
          Add Comment
        </button>
        <div class="btn-group">
          <button
            type="button"
            class="btn btn-light btn-sm dropdown-toggle"
            data-bs-toggle="dropdown"
          >
            <KTIcon icon-name="filter" icon-class="fs-6" />
            Filter
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#" @click="filterType = 'all'">All Activity</a></li>
            <li><a class="dropdown-item" href="#" @click="filterType = 'comments'">Comments Only</a></li>
            <li><a class="dropdown-item" href="#" @click="filterType = 'changes'">Changes Only</a></li>
            <li><a class="dropdown-item" href="#" @click="filterType = 'documents'">Documents Only</a></li>
            <li><a class="dropdown-item" href="#" @click="filterType = 'system'">System Events</a></li>
          </ul>
        </div>
      </div>
      <!--end::Card toolbar-->
    </div>
    <!--end::Card header-->

    <!--begin::Card body-->
    <div class="card-body pt-0">
      <!--begin::Loading-->
      <div v-if="loading" class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <!--end::Loading-->

      <!--begin::Add Comment Form-->
      <div v-if="showAddComment && !loading" class="card border border-dashed border-primary mb-6">
        <div class="card-body">
          <div class="d-flex align-items-start">
            <!--begin::Avatar-->
            <div class="symbol symbol-40px symbol-circle me-4">
              <span class="symbol-label bg-light-primary text-primary fw-bold fs-6">
                {{ getCurrentUserInitials() }}
              </span>
            </div>
            <!--end::Avatar-->

            <!--begin::Form-->
            <div class="flex-grow-1">
              <textarea
                v-model="newComment"
                class="form-control form-control-solid"
                rows="3"
                placeholder="Add a comment..."
              ></textarea>
              <div class="d-flex justify-content-end mt-3">
                <button
                  class="btn btn-light btn-sm me-2"
                  @click="cancelComment"
                >
                  Cancel
                </button>
                <button
                  class="btn btn-primary btn-sm"
                  @click="addComment"
                  :disabled="!newComment.trim() || isSubmitting"
                >
                  <span v-if="!isSubmitting">Add Comment</span>
                  <span v-else>
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    Adding...
                  </span>
                </button>
              </div>
            </div>
            <!--end::Form-->
          </div>
        </div>
      </div>
      <!--end::Add Comment Form-->

      <!--begin::Activity Timeline-->
      <div v-if="!loading" class="timeline timeline-border-dashed">
        <!--begin::Timeline item-->
        <div
          v-for="(item, index) in filteredActivity"
          :key="item.id || index"
          class="timeline-item"
        >
          <!--begin::Timeline line-->
          <div class="timeline-line"></div>
          <!--end::Timeline line-->

          <!--begin::Timeline icon-->
          <div class="timeline-icon">
            <i :class="getTimelineIcon(item.type)">
              <span class="path1"></span>
              <span class="path2"></span>
              <span class="path3" v-if="item.type === 'comment' || item.type === 'system' || item.type === 'document'"></span>
              <span class="path4" v-if="item.type === 'system' || item.type === 'document'"></span>
              <span class="path5" v-if="item.type === 'system' || item.type === 'document'"></span>
            </i>
          </div>
          <!--end::Timeline icon-->

          <!--begin::Timeline content-->
          <div class="timeline-content mb-10 mt-n1">
            <!--begin::Timeline heading-->
            <div class="pe-3 mb-5">
              <!--begin::Title-->
              <div class="fs-5 fw-semibold mb-2">
                {{ getActivityTitle(item) }}
              </div>
              <!--end::Title-->

              <!--begin::User Info-->
              <div class="d-flex align-items-center mt-1 fs-6">
                <!--begin::Info-->
                <div class="text-muted me-2 fs-7">
                  Added at {{ formatTime(item.created_at || item.timestamp) }} by
                </div>
                <!--end::Info-->

                <!--begin::User-->
                <div class="symbol symbol-circle symbol-25px me-2" data-bs-toggle="tooltip" :title="getUserName(item.user || item.created_by)">
                  <span class="symbol-label bg-light-primary text-primary fw-bold fs-8">
                    {{ getUserInitials(item.user || item.created_by) }}
                  </span>
                </div>
                <!--end::User-->

                <!--begin::User Name-->
                <div class="text-gray-800 fw-semibold fs-7">
                  {{ getUserName(item.user || item.created_by) }}
                </div>
                <!--end::User Name-->
              </div>
              <!--end::User Info-->

              <!--begin::Description-->
              <div class="overflow-auto pb-5">
                <div v-if="item.type === 'comment'" class="mt-3">
                  <div class="notice d-flex bg-light-primary rounded border-primary border border-dashed p-6">
                    <div class="d-flex flex-stack flex-grow-1">
                      <div class="fw-semibold">
                        <div class="text-gray-900 fs-6">{{ item.text || item.comment || item.content }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else-if="item.type === 'modification'" class="text-gray-700">
                  <!-- Remove redundant message since it's now in the title -->
                </div>
                <div v-else-if="item.type === 'change'" class="text-gray-700">
                  <div class="fw-semibold text-gray-900 mb-2">{{ item.description }}</div>
                  <div v-if="item.changes" class="bg-light-info p-3 rounded">
                    <div v-for="(change, changeIndex) in item.changes" :key="changeIndex" class="mb-1">
                      <span class="fw-semibold">{{ change.field }}:</span>
                      <span v-if="change.old_value" class="text-danger ms-1">{{ change.old_value }}</span>
                      <span v-if="change.old_value" class="text-muted mx-1">→</span>
                      <span class="text-success">{{ change.new_value }}</span>
                    </div>
                  </div>
                </div>
                <div v-else-if="item.type === 'document'" class="text-gray-700">
                  {{ item.description || 'Document activity' }}
                </div>
                <div v-else-if="item.type === 'system'" class="text-gray-600">
                  {{ item.description || item.message }}
                </div>
                <div v-else class="text-gray-700">
                  {{ item.description || item.content || 'Activity recorded' }}
                </div>
              </div>
              <!--end::Description-->
            </div>
            <!--end::Timeline heading-->

            <!--begin::Timeline details-->
            <div v-if="item.type === 'modification'" class="overflow-auto pb-5">
              <div class="d-flex align-items-center border border-dashed border-gray-300 rounded min-w-700px p-5">
                <!--begin::Item-->
                <div class="d-flex flex-aligns-center">
                  <!--begin::Icon-->
                  <img
                    v-if="getModificationIcon(item.field)"
                    alt="Field Change"
                    class="w-30px me-3"
                    :src="getModificationIcon(item.field)"
                  >
                  <!--end::Icon-->

                  <!--begin::Info-->
                  <div class="ms-1 fw-semibold" :class="{ 'ms-0': !getModificationIcon(item.field) }">
                    <!--begin::Desc-->
                    <div class="fs-6 fw-bold text-gray-800">
                      {{ formatFieldName(item.field) }}
                    </div>
                    <!--end::Desc-->

                    <!--begin::Change Details-->
                    <div class="text-gray-600 fs-7">
                      <span v-if="item.before" class="text-danger">{{ formatFieldValue(item.before) }}</span>
                      <span v-if="item.before" class="text-muted mx-2">→</span>
                      <span class="text-success">{{ formatFieldValue(item.after) }}</span>
                    </div>
                    <!--end::Change Details-->
                  </div>
                  <!--end::Info-->
                </div>
                <!--end::Item-->
              </div>
            </div>

            <div v-else-if="item.type === 'document' && item.documents && item.documents.length > 0" class="overflow-auto pb-5">
              <div class="d-flex align-items-center border border-dashed border-gray-300 rounded min-w-700px p-5">
                <!--begin::Document Items-->
                <div
                  v-for="(doc, docIndex) in item.documents"
                  :key="docIndex"
                  class="d-flex flex-aligns-center"
                  :class="{ 'pe-10 pe-lg-20': docIndex < item.documents.length - 1 }"
                >
                  <!--begin::Icon-->
                  <img
                    :alt="doc.name || 'Document'"
                    class="w-30px me-3"
                    :src="getDocumentIcon(doc.file_type || doc.type)"
                  >
                  <!--end::Icon-->

                  <!--begin::Info-->
                  <div class="ms-1 fw-semibold">
                    <!--begin::Desc-->
                    <a
                      :href="doc.download_url || doc.url"
                      class="fs-6 text-hover-primary fw-bold"
                      target="_blank"
                    >
                      {{ doc.name || doc.filename || 'Document' }}
                    </a>
                    <!--end::Desc-->

                    <!--begin::Size-->
                    <div class="text-gray-500">{{ formatFileSize(doc.size) }}</div>
                    <!--end::Size-->
                  </div>
                  <!--end::Info-->
                </div>
                <!--end::Document Items-->
              </div>
            </div>
            <!--end::Timeline details-->

            <!--begin::Action-->
            <div v-if="item.type === 'comment' && canDeleteComment(item)" class="d-flex justify-content-end mt-3">
              <button
                class="btn btn-icon btn-active-light-danger btn-sm"
                @click="deleteComment(item)"
                title="Delete comment"
              >
                <KTIcon icon-name="trash" icon-class="fs-7" />
              </button>
            </div>
            <!--end::Action-->
          </div>
          <!--end::Timeline content-->
        </div>
        <!--end::Timeline item-->
      </div>
      <!--end::Activity Timeline-->

      <!--begin::No Activity-->
      <div v-if="!loading && filteredActivity.length === 0" class="alert alert-light-info">
        <div class="d-flex align-items-center">
          <KTIcon icon-name="information" icon-class="fs-2 text-info me-3" />
          <div>
            <h5 class="text-info mb-1">No Activity Found</h5>
            <span class="text-gray-700">
              <span v-if="filterType === 'all'">There is no activity recorded for this trip yet.</span>
              <span v-else>No {{ filterType }} found for this trip.</span>
            </span>
          </div>
        </div>
      </div>
      <!--end::No Activity-->

      <!--begin::Load More-->
      <div v-if="!loading && hasMore" class="text-center mt-8">
        <button
          class="btn btn-light-primary btn-sm"
          @click="loadMoreActivity"
          :disabled="loadingMore"
        >
          <span v-if="!loadingMore">Load More Activity</span>
          <span v-else>
            <span class="spinner-border spinner-border-sm me-2"></span>
            Loading...
          </span>
        </button>
      </div>
      <!--end::Load More-->
    </div>
    <!--end::Card body-->
  </div>
  <!--end::Activity Card-->
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import ApiService from '@/core/services/ApiService';
import { useAuthStore } from '@/stores/auth';
import Swal from 'sweetalert2';

interface Props {
  trip: any;
  loading: boolean;
}

const props = defineProps<Props>();
const authStore = useAuthStore();

const activity = ref<any[]>([]);
const showAddComment = ref(false);
const newComment = ref('');
const isSubmitting = ref(false);
const loading = ref(false);
const loadingMore = ref(false);
const hasMore = ref(true);
const filterType = ref<'all' | 'comments' | 'changes' | 'documents' | 'system'>('all');
const currentPage = ref(1);

// Computed properties
const filteredActivity = computed(() => {
  if (filterType.value === 'all') {
    return activity.value;
  }

  return activity.value.filter(item => {
    switch (filterType.value) {
      case 'comments':
        return item.type === 'comment';
      case 'changes':
        return item.type === 'change' || item.type === 'modification';
      case 'documents':
        return item.type === 'document';
      case 'system':
        return item.type === 'system' || item.type === 'status_change';
      default:
        return true;
    }
  });
});

// Load activity data using simplified approach like TripComments.vue
const loadActivity = async () => {
  if (!props.trip?.id) return;

  loading.value = true;

  try {
    // Load comments and modifications separately using the working pattern
    await Promise.all([
      fetchComments(),
      fetchModifications()
    ]);
  } catch (error) {
    console.error('Error loading activity:', error);
  } finally {
    loading.value = false;
  }
};

const fetchComments = async () => {
  try {
    console.log('🔍 Fetching comments for trip:', props.trip.id);

    // Trip comments
    const { data: tripComments } = await ApiService.get(`/comments/for_object/?model=trip&object_id=${props.trip.id}`);
    console.log('✅ Trip comments:', tripComments);

    let allComments = [...(tripComments || [])];

    // Quote comments (if trip has a quote)
    if (props.trip.quote?.id) {
      try {
        console.log('📈 Fetching quote comments for:', props.trip.quote.id);
        const { data: quoteComments } = await ApiService.get(`/comments/for_object/?model=quote&object_id=${props.trip.quote.id}`);
        console.log('✅ Quote comments:', quoteComments);
        allComments = allComments.concat((quoteComments || []).map((comment: any) => ({
          ...comment,
          entity_type: 'quote',
          entity_name: 'Quote'
        })));
      } catch (error) {
        console.warn('❌ Error loading quote comments:', error);
      }
    }

    // Patient comments (if trip has a patient)
    if (props.trip.patient?.id) {
      try {
        console.log('🏥 Fetching patient comments for:', props.trip.patient.id);
        const { data: patientComments } = await ApiService.get(`/comments/for_object/?model=patient&object_id=${props.trip.patient.id}`);
        console.log('✅ Patient comments:', patientComments);
        allComments = allComments.concat((patientComments || []).map((comment: any) => ({
          ...comment,
          entity_type: 'patient',
          entity_name: 'Patient'
        })));
      } catch (error) {
        console.warn('❌ Error loading patient comments:', error);
      }
    }

    console.log('📝 Total comments found:', allComments.length);

    // Add comments to activity
    allComments.forEach(comment => {
      activity.value.push({
        id: comment.id,
        type: 'comment',
        entity_type: comment.entity_type || 'trip',
        entity_name: comment.entity_name || 'Trip',
        text: comment.text,
        timestamp: comment.created_on,
        created_at: comment.created_on,
        user: {
          created_by_name: comment.created_by_name,
          created_by_username: comment.created_by_username,
          id: comment.created_by
        },
        created_by: {
          created_by_name: comment.created_by_name,
          created_by_username: comment.created_by_username,
          id: comment.created_by
        }
      });
    });
  } catch (error) {
    console.error('💥 Error fetching comments:', error);
  }
};

const fetchModifications = async () => {
  try {
    // Trip modifications
    const { data: tripMods } = await ApiService.get(`/modifications/for_object/?model=Trip&object_id=${props.trip.id}`);

    let allModifications = [...(tripMods || [])];

    // Quote modifications (if trip has a quote)
    if (props.trip.quote?.id) {
      try {
        const { data: quoteMods } = await ApiService.get(`/modifications/for_object/?model=Quote&object_id=${props.trip.quote.id}`);
        allModifications = allModifications.concat((quoteMods || []).map((mod: any) => ({
          ...mod,
          entity_type: 'quote',
          entity_name: 'Quote'
        })));
      } catch (error) {
        console.warn('Error loading quote modifications:', error);
      }
    }

    // Patient modifications (if trip has a patient)
    if (props.trip.patient?.id) {
      try {
        const { data: patientMods } = await ApiService.get(`/modifications/for_object/?model=Patient&object_id=${props.trip.patient.id}`);
        allModifications = allModifications.concat((patientMods || []).map((mod: any) => ({
          ...mod,
          entity_type: 'patient',
          entity_name: 'Patient'
        })));
      } catch (error) {
        console.warn('Error loading patient modifications:', error);
      }
    }

    // Add modifications to activity
    allModifications.forEach(mod => {
      let type: 'modification' | 'creation' | 'deletion' = 'modification';
      if (mod.field === '__created__') type = 'creation';
      else if (mod.field === '__deleted__') type = 'deletion';

      // Structure user data properly for the display functions
      const userObj = mod.user ? {
        id: mod.user,
        username: mod.user_username || 'unknown',
        first_name: mod.user_name ? mod.user_name.split(' ')[0] : '',
        last_name: mod.user_name ? mod.user_name.split(' ').slice(1).join(' ') : '',
        full_name: mod.user_name || mod.user_username || 'Unknown User'
      } : null;

      activity.value.push({
        id: mod.id,
        type,
        entity_type: mod.entity_type || 'trip',
        entity_name: mod.entity_name || 'Trip',
        field: mod.field,
        before: mod.before,
        after: mod.after,
        timestamp: mod.time,
        created_at: mod.time,
        user: userObj,
        created_by: userObj
      });
    });

    // Sort all activity by timestamp (newest first)
    activity.value.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  } catch (error) {
    console.error('Error fetching modifications:', error);
  }
};

const loadMoreActivity = async () => {
  // Pagination disabled for now since we load all data at once
  loadingMore.value = false;
};

// Content type mapping (from TripComments.vue working implementation)
const getContentTypeId = (entityType: string): number => {
  const contentTypeMap: Record<string, number> = {
    'quote': 22,
    'trip': 23,
    'patient': 17,
    'contact': 9,
    'passenger': 18,
    'aircraft': 15,
    'fbo': 10,
  };
  return contentTypeMap[entityType] || 23; // Default to trip
};

// Comment management
const addComment = async () => {
  if (!newComment.value.trim() || isSubmitting.value) return;

  isSubmitting.value = true;
  console.log('💬 Adding comment to trip:', props.trip.id);

  try {
    // Use the working pattern from TripComments.vue
    const response = await ApiService.post('/comments/', {
      content_type: getContentTypeId('trip'),
      object_id: props.trip.id,
      text: newComment.value.trim()
    });

    console.log('✅ Comment created:', response.data);

    // Add the new comment to the beginning of the activity list
    activity.value.unshift({
      id: response.data.id,
      type: 'comment',
      text: response.data.text,
      entity_type: 'trip',
      entity_name: 'Trip',
      created_on: response.data.created_on,
      timestamp: response.data.created_on,
      created_at: response.data.created_on,
      user: response.data.created_by || authStore.user,
      created_by: response.data.created_by || authStore.user
    });

    newComment.value = '';
    showAddComment.value = false;

    Swal.fire({
      title: 'Comment Added',
      text: 'Your comment has been posted successfully',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('❌ Error adding comment:', error);
    Swal.fire({
      title: 'Error',
      text: 'Failed to add comment. Please try again.',
      icon: 'error'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const cancelComment = () => {
  newComment.value = '';
  showAddComment.value = false;
};

const deleteComment = async (comment: any) => {
  const result = await Swal.fire({
    title: 'Delete Comment?',
    text: 'Are you sure you want to delete this comment? This action cannot be undone.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    try {
      await ApiService.delete(`comments/${comment.id}/`);

      // Remove comment from activity list
      const index = activity.value.findIndex(item => item.id === comment.id);
      if (index > -1) {
        activity.value.splice(index, 1);
      }

      Swal.fire('Deleted!', 'Comment has been deleted.', 'success');
    } catch (error) {
      console.error('Error deleting comment:', error);
      Swal.fire('Error', 'Failed to delete comment.', 'error');
    }
  }
};

// Helper functions
const getCurrentUserInitials = (): string => {
  const user = authStore.user;
  if (!user) return '?';

  const first = user.first_name || '';
  const last = user.last_name || '';

  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

const getUserInitials = (user: any): string => {
  if (!user) return '?';

  // Handle comment data structure (created_by_name from CommentSerializer)
  if (user.created_by_name) {
    const parts = user.created_by_name.split(' ');
    return parts.map(part => part.charAt(0)).slice(0, 2).join('').toUpperCase() || '?';
  }

  // Handle modification data structure (full_name from ModificationSerializer)
  if (user.full_name) {
    const parts = user.full_name.split(' ');
    return parts.map(part => part.charAt(0)).slice(0, 2).join('').toUpperCase() || '?';
  }

  // Handle direct user object
  const first = user.first_name || '';
  const last = user.last_name || '';

  return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
};

const getUserName = (user: any): string => {
  if (!user) return 'Unknown User';

  // Handle comment data structure (created_by_name from CommentSerializer)
  if (user.created_by_name) return user.created_by_name;

  // Handle username fallback for comments
  if (user.created_by_username) return user.created_by_username;

  // Handle modification data structure (full_name from ModificationSerializer)
  if (user.full_name) return user.full_name;

  // Handle direct user object
  const first = user.first_name || '';
  const last = user.last_name || '';

  return `${first} ${last}`.trim() || user.username || 'Unknown User';
};

const getUserRole = (user: any): string => {
  if (!user) return '';

  return user.role || user.user_type || 'User';
};

const canDeleteComment = (comment: any): boolean => {
  const currentUser = authStore.user;
  if (!currentUser || !comment.user) return false;

  // User can delete their own comments, or admins can delete any
  return comment.user.id === currentUser.id || currentUser.is_staff;
};

const getActivityTitle = (item: any): string => {
  switch (item.type) {
    case 'comment':
      return `Comment Added ${item.entity_name ? 'to ' + item.entity_name : ''}`;
    case 'modification':
      const entityName = item.entity_name || 'Record';
      const fieldName = formatFieldName(item.field);
      const action = item.before ? 'changed' : 'set';
      return `${entityName}: ${fieldName} ${action}`;
    case 'change':
      return item.title || 'Record Modified';
    case 'document':
      const docCount = item.documents ? item.documents.length : 1;
      return `${docCount} New Document${docCount > 1 ? 's' : ''} Added`;
    case 'system':
      return item.title || 'System Event';
    case 'status_change':
      return 'Status Changed';
    default:
      return 'Activity';
  }
};

const getTimelineIcon = (type: string): string => {
  switch (type) {
    case 'comment':
      return 'ki-duotone ki-message-text-2 fs-2 text-gray-500';
    case 'change':
    case 'modification':
      return 'ki-duotone ki-pencil fs-2 text-gray-500';
    case 'creation':
      return 'ki-duotone ki-plus fs-2 text-gray-500';
    case 'deletion':
      return 'ki-duotone ki-trash fs-2 text-gray-500';
    case 'document':
      return 'ki-duotone ki-disconnect fs-2 text-gray-500';
    case 'system':
      return 'ki-duotone ki-abstract-26 fs-2 text-gray-500';
    case 'status_change':
      return 'ki-duotone ki-flag fs-2 text-gray-500';
    default:
      return 'ki-duotone ki-sms fs-2 text-gray-500';
  }
};

const getDocumentIcon = (fileType: string): string => {
  if (!fileType) return '/media/svg/files/doc.svg';

  const type = fileType.toLowerCase();

  if (type.includes('pdf')) return '/media/svg/files/pdf.svg';
  if (type.includes('doc') || type.includes('word')) return '/media/svg/files/doc.svg';
  if (type.includes('xls') || type.includes('excel')) return '/media/svg/files/xls.svg';
  if (type.includes('ppt') || type.includes('powerpoint')) return '/media/svg/files/ppt.svg';
  if (type.includes('image') || type.includes('jpg') || type.includes('png') || type.includes('gif')) return '/media/svg/files/img.svg';
  if (type.includes('video') || type.includes('mp4') || type.includes('avi')) return '/media/svg/files/vid.svg';
  if (type.includes('audio') || type.includes('mp3') || type.includes('wav')) return '/media/svg/files/aud.svg';
  if (type.includes('zip') || type.includes('rar') || type.includes('archive')) return '/media/svg/files/zip.svg';
  if (type.includes('css')) return '/media/svg/files/css.svg';
  if (type.includes('html')) return '/media/svg/files/html.svg';
  if (type.includes('js') || type.includes('javascript')) return '/media/svg/files/js.svg';

  return '/media/svg/files/doc.svg';
};

const formatFileSize = (bytes: number): string => {
  if (!bytes || bytes === 0) return '0 KB';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
};

const getModificationIcon = (field: string): string => {
  if (!field) return null;

  const fieldLower = field.toLowerCase();

  // Special image fields that should use blank-image.svg
  if (fieldLower.includes('insurance_card') || fieldLower.includes('insurance card')) return '/media/svg/files/blank-image.svg';
  if (fieldLower.includes('letter_of_medical_necessity') || fieldLower.includes('letter of medical necessity')) return '/media/svg/files/blank-image.svg';

  // Document/file-related fields that should show icons
  if (fieldLower.includes('document') || fieldLower.includes('file') || fieldLower.includes('attachment')) return '/media/svg/files/doc.svg';
  if (fieldLower.includes('image') || fieldLower.includes('photo') || fieldLower.includes('picture')) return '/media/svg/files/blank-image.svg';
  if (fieldLower.includes('pdf')) return '/media/svg/files/pdf.svg';

  // For non-document/non-image fields, return null to hide the icon
  return null;
};

const formatDateTime = (datetime: string): string => {
  if (!datetime) return '';

  try {
    const date = new Date(datetime);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return 'Yesterday at ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays < 7) {
      return date.toLocaleDateString([], { weekday: 'long' }) + ' at ' +
             date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString() + ' at ' +
             date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
  } catch (error) {
    return datetime;
  }
};

const formatTime = (datetime: string): string => {
  if (!datetime) return '';

  try {
    const date = new Date(datetime);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch (error) {
    return datetime;
  }
};

const formatFieldName = (field: string): string => {
  if (!field) return 'Field';

  // Handle special field names
  const fieldMap: Record<string, string> = {
    'trip_number': 'Trip Number',
    'estimated_departure_time': 'Departure Time',
    'quoted_amount': 'Quote Amount',
    'pickup_airport': 'Pickup Airport',
    'dropoff_airport': 'Dropoff Airport',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'date_of_birth': 'Date of Birth',
    'phone_number': 'Phone Number',
    'email_address': 'Email Address',
    'medical_team': 'Medical Team',
    'aircraft_type': 'Aircraft Type',
    'pre_flight_duty_time': 'Pre-flight Duty Time',
    'post_flight_duty_time': 'Post-flight Duty Time',
    '__created__': 'Record Created',
    '__deleted__': 'Record Deleted'
  };

  if (fieldMap[field]) {
    return fieldMap[field];
  }

  // Convert snake_case to Title Case
  return field
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const formatFieldValue = (value: any): string => {
  if (value === null || value === undefined) return 'None';
  if (value === '') return 'Empty';
  if (typeof value === 'boolean') return value ? 'Yes' : 'No';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
};

// Load activity on mount and when trip changes
onMounted(() => {
  if (props.trip?.id) {
    // Clear existing activity first
    activity.value = [];
    loadActivity();
  }
});

// Watch for changes in trip ID
watch(() => props.trip?.id, (newTripId) => {
  if (newTripId) {
    // Clear existing activity first
    activity.value = [];
    loadActivity();
  }
}, { immediate: false });
</script>

<style scoped>
/* Use Metronic's built-in timeline styles */
/* Add any custom styles only if needed */
</style>