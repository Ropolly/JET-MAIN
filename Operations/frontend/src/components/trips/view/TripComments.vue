<template>
  <div class="card mb-5 mb-xxl-8">
    <!--begin::Header-->
    <div class="card-header align-items-center border-0 mt-4">
      <h3 class="card-title align-items-start flex-column">
        <span class="fw-bold mb-2 text-gray-900">Updates</span>
        <span class="text-muted fw-semibold fs-7">Comments and actions taken on trip</span>
      </h3>
    </div>
    <!--end::Header-->
    
    <!-- Comment Form -->
    <div style="padding: 0px 29.25px 0px 29.25px">
      <form @submit.prevent="submitComment" id="comment-form">
        <div class="col-xl-12 fv-row fv-plugins-icon-container">
          <input 
            class="form-control form-control-solid comment-field" 
            v-model="commentText"
            placeholder="Write an update" 
            required 
            type="text"
            @focus="showSubmitButton = true"
          />
          <div class="fv-plugins-message-container invalid-feedback"></div>
        </div>
        
        <div class="d-flex justify-content-end py-2" v-show="showSubmitButton">
          <button 
            class="btn btn-primary comment-submit" 
            type="submit" 
            :disabled="isSubmitting || !commentText.trim()"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ isSubmitting ? 'Posting...' : 'Update' }}
          </button>
        </div>
      </form>
    </div>
    
    <!--begin::Body-->
    <div class="card-body pt-5 pb-9" style="max-height:450px; overflow: scroll;">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <span class="spinner-border spinner-border-lg"></span>
        <div class="text-muted mt-3">Loading updates...</div>
      </div>
      
      <!-- Timeline -->
      <div v-else-if="timelineItems.length > 0" class="tab-pane fade show active" id="kt_timeline" role="tabpanel">
        <div 
          v-for="(item, index) in timelineItems" 
          :key="`${item.type}-${item.id}`"
          class="d-flex justify-content-between position-relative mb-5"
        >
          <!--begin::Bar-->
          <div 
            class="position-absolute h-100 w-4px rounded top-0 start-0"
            :class="getTimelineBarColor(item)"
          ></div>
          <!--end::Bar-->

          <!--begin::Info-->
          <div class="fw-semibold ms-5 text-gray-600" style="max-width:78%;">
            <a class="fs-6 fw-bold text-gray-600 text-hover-primary mb-2" href="#">
              {{ getTimelineTitle(item) }}
            </a>
            
            <!--begin::Content-->
            <div class="text-gray-500">
              {{ getTimelineContent(item) }}
            </div>
            <!--end::Content-->
          </div>
          <!--end::Info-->

          <!--begin::Action-->
          <div class="text-gray-500 fs-7 text-end">
            {{ formatTimeAgo(item.timestamp) }}
          </div>
          <!--end::Action-->
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="text-center py-10">
        <KTIcon icon-name="file-text" icon-class="fs-3x text-muted mb-4" />
        <div class="text-muted fs-6">No updates yet</div>
        <div class="text-muted fs-7">Be the first to add a comment</div>
      </div>
    </div>
    <!--end: Card Body-->
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';
import { formatDistanceToNow, parseISO } from 'date-fns';

interface Props {
  tripId: string;
  tripData?: any; // Optional trip data to extract creation info
}

interface Comment {
  id: string;
  text: string;
  created_on: string;
  created_by_username?: string;
  created_by_name?: string;
}

interface Modification {
  id: string;
  field: string;
  before?: string;
  after?: string;
  time: string;
  user_username?: string;
  user_name?: string;
}

interface TimelineItem {
  id: string;
  type: 'comment' | 'modification' | 'creation' | 'deletion';
  timestamp: string;
  user: string;
  data: Comment | Modification;
}

const props = withDefaults(defineProps<Props>(), {});

// Reactive state
const commentText = ref('');
const showSubmitButton = ref(false);
const isSubmitting = ref(false);
const loading = ref(false);
const comments = ref<Comment[]>([]);
const modifications = ref<Modification[]>([]);

// Computed timeline items
const timelineItems = computed<TimelineItem[]>(() => {
  const items: TimelineItem[] = [];
  
  // Add trip creation from tripData if available and no creation modification exists
  if (props.tripData?.created_on) {
    const hasCreationMod = modifications.value.some(mod => mod.field === '__created__');
    
    if (!hasCreationMod) {
      items.push({
        id: `creation-${props.tripId}`,
        type: 'creation',
        timestamp: props.tripData.created_on,
        user: props.tripData.created_by_name || 
              props.tripData.created_by?.username || 
              (props.tripData.created_by?.first_name && props.tripData.created_by?.last_name 
                ? `${props.tripData.created_by.first_name} ${props.tripData.created_by.last_name}`.trim()
                : props.tripData.created_by?.first_name || props.tripData.created_by?.last_name) ||
              'System',
        data: {
          field: '__created__',
          after: 'Instance created'
        }
      });
    }
  }
  
  // Add comments
  comments.value.forEach(comment => {
    items.push({
      id: comment.id,
      type: 'comment',
      timestamp: comment.created_on,
      user: comment.created_by_name || comment.created_by_username || 'Unknown User',
      data: comment
    });
  });
  
  // Add modifications
  modifications.value.forEach(mod => {
    let type: 'modification' | 'creation' | 'deletion' = 'modification';
    if (mod.field === '__created__') type = 'creation';
    else if (mod.field === '__deleted__') type = 'deletion';
    
    items.push({
      id: mod.id,
      type,
      timestamp: mod.time,
      user: mod.user_name || mod.user_username || 'System',
      data: mod
    });
  });
  
  // Sort by timestamp (newest first)
  return items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
});

// Methods
const getTimelineBarColor = (item: TimelineItem): string => {
  switch (item.type) {
    case 'comment': return 'bg-primary';
    case 'creation': return 'bg-success';
    case 'deletion': return 'bg-danger';
    case 'modification': return 'bg-warning';
    default: return 'bg-secondary';
  }
};

const formatFieldName = (fieldName: string): string => {
  return fieldName
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const getTimelineTitle = (item: TimelineItem): string => {
  switch (item.type) {
    case 'comment':
      return `${item.user} added a comment`;
    case 'creation':
      return `${item.user} created trip`;
    case 'deletion':
      return `${item.user} deleted trip`;
    case 'modification':
      const mod = item.data as Modification;
      const formattedField = formatFieldName(mod.field);
      return `${item.user} updated ${formattedField}`;
    default:
      return `${item.user} performed an action`;
  }
};

const getTimelineContent = (item: TimelineItem): string => {
  switch (item.type) {
    case 'comment':
      const comment = item.data as Comment;
      return comment.text;
    case 'creation':
      return 'Trip was created and is now available in the system';
    case 'deletion':
      return 'Trip was deleted';
    case 'modification':
      const mod = item.data as Modification;
      if (mod.before && mod.after) {
        return `Changed from "${mod.before}" to "${mod.after}"`;
      } else if (mod.after) {
        return `Set to "${mod.after}"`;
      } else if (mod.before) {
        return `Removed "${mod.before}"`;
      }
      return 'Field was updated';
    default:
      return '';
  }
};

const formatTimeAgo = (timestamp: string): string => {
  try {
    return formatDistanceToNow(parseISO(timestamp), { addSuffix: true });
  } catch (error) {
    return 'Unknown time';
  }
};

const fetchComments = async () => {
  try {
    const { data } = await ApiService.get(`/comments/for_object/?model=trip&object_id=${props.tripId}`);
    comments.value = data || [];
  } catch (error) {
    console.error('Error fetching comments:', error);
    comments.value = [];
  }
};

const fetchModifications = async () => {
  try {
    const { data } = await ApiService.get(`/modifications/for_object/?model=Trip&object_id=${props.tripId}`);
    modifications.value = data || [];
  } catch (error) {
    console.error('Error fetching modifications:', error);
    modifications.value = [];
  }
};

const submitComment = async () => {
  if (!commentText.value.trim()) return;
  
  isSubmitting.value = true;
  
  try {
    // Create comment using content type ID
    await ApiService.post('/comments/', {
      content_type: getContentTypeId('trip'),
      object_id: props.tripId,
      text: commentText.value.trim()
    });
    
    // Reset form
    commentText.value = '';
    showSubmitButton.value = false;
    
    // Refresh comments
    await fetchComments();
    
    Swal.fire({
      title: 'Comment Added',
      text: 'Your comment has been posted successfully',
      icon: 'success',
      timer: 2000,
      showConfirmButton: false
    });
    
  } catch (error) {
    console.error('Error posting comment:', error);
    Swal.fire({
      title: 'Error',
      text: 'Failed to post comment. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const getContentTypeId = (entityType: string): number => {
  // Map entity types to content type IDs
  const contentTypeMap: Record<string, number> = {
    'quote': 22,
    'trip': 23,
    'patient': 17,
    'contact': 9,
    'passenger': 18,
    'aircraft': 15,
    'fbo': 10,
    // Add more mappings as needed
  };
  return contentTypeMap[entityType] || 1;
};

const loadData = async () => {
  loading.value = true;
  try {
    await Promise.all([
      fetchComments(),
      fetchModifications()
    ]);
  } finally {
    loading.value = false;
  }
};

// Watch for changes in trip ID
watch(() => props.tripId, () => {
  if (props.tripId) {
    loadData();
  }
}, { immediate: true });

onMounted(() => {
  if (props.tripId) {
    loadData();
  }
});

// Expose methods for parent component
defineExpose({
  refresh: loadData
});
</script>

<style scoped>
.comment-field:focus + .d-flex {
  display: flex !important;
}

.spinner-border-lg {
  width: 3rem;
  height: 3rem;
}
</style>