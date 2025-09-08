<template>
  <div class="card mt-5 mb-5">
    <div class="card-header">
      <h3 class="card-title">
        <span class="fw-bold">Updates & Comments</span>
        <span class="text-muted fw-semibold fs-7 ms-2">Activity on this quote</span>
      </h3>
      <div class="card-toolbar">
        <button
          type="button"
          class="btn btn-sm btn-light-primary"
          @click="toggleAddComment"
        >
          <i class="fas fa-plus fs-4 me-2"></i>
          Add Comment
        </button>
      </div>
    </div>
    <div class="card-body">
      <!-- Add Comment Form -->
      <div v-if="showAddComment" class="mb-5">
        <div class="d-flex">
          <textarea
            v-model="newCommentText"
            class="form-control"
            rows="3"
            placeholder="Add a comment..."
            @keydown.ctrl.enter="submitComment"
          ></textarea>
        </div>
        <div class="d-flex justify-content-end mt-3 gap-2">
          <button
            type="button"
            class="btn btn-sm btn-light"
            @click="cancelAddComment"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-sm btn-primary"
            @click="submitComment"
            :disabled="!newCommentText.trim() || isSubmitting"
          >
            <span v-if="isSubmitting">
              <span class="spinner-border spinner-border-sm me-2" role="status"></span>
              Posting...
            </span>
            <span v-else>
              Post Comment
            </span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="d-flex justify-content-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Timeline & Comments List -->
      <div v-else-if="timelineItems.length > 0" class="timeline-list" style="max-height: 500px; overflow-y: auto;">
        <div
          v-for="item in timelineItems"
          :key="`${item.type}-${item.id}`"
          class="d-flex align-items-start mb-4"
        >
          <!-- Avatar/Icon -->
          <div class="symbol symbol-35px me-3">
            <div 
              class="symbol-label fw-semibold"
              :class="getAvatarClass(item)"
            >
              <i v-if="item.type !== 'comment'" :class="getTimelineIcon(item)" class="fs-7"></i>
              <span v-else>{{ getInitials(item.user) }}</span>
            </div>
          </div>
          
          <!-- Content -->
          <div class="flex-grow-1">
            <div 
              class="rounded p-3"
              :class="item.type === 'comment' ? 'bg-light-gray-100' : ''"
            >
              <!-- Header -->
              <div class="d-flex justify-content-between align-items-center mb-2">
                <div>
                  <span class="fw-bold text-gray-900">
                    {{ item.user }}
                  </span>
                  <span class="text-muted ms-2 fs-7">
                    {{ getActionText(item) }}
                  </span>
                  <span class="text-muted ms-2 fs-7">
                    {{ formatDate(item.timestamp) }}
                  </span>
                </div>
                <div class="dropdown" v-if="item.type === 'comment' && canEditComment(item)">
                  <button
                    class="btn btn-sm btn-light-primary btn-icon dropdown-toggle"
                    type="button"
                    data-bs-toggle="dropdown"
                  >
                    <i class="fas fa-ellipsis-h fs-7"></i>
                  </button>
                  <ul class="dropdown-menu">
                    <li>
                      <a class="dropdown-item" href="#" @click.prevent="editComment(item)">
                        <i class="fas fa-edit me-2"></i>Edit
                      </a>
                    </li>
                    <li>
                      <a class="dropdown-item text-danger" href="#" @click.prevent="deleteComment(item)">
                        <i class="fas fa-trash me-2"></i>Delete
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
              
              <!-- Content -->
              <div v-if="editingCommentId !== item.id" class="text-gray-700">
                <div v-if="item.type === 'comment'">
                  {{ item.data.text }}
                </div>
                <div v-else-if="item.type === 'modification'" class="fs-7">
                  <span class="text-muted">{{ formatFieldName(item.data.field) }}:</span>
                  <span v-if="item.data.before && item.data.after" class="ms-2">
                    <span class="text-danger text-decoration-line-through">{{ item.data.before }}</span>
                    <i class="fas fa-arrow-right mx-2 text-muted fs-8"></i>
                    <span class="text-success">{{ item.data.after }}</span>
                  </span>
                  <span v-else-if="item.data.after" class="text-success ms-2">
                    Set to "{{ item.data.after }}"
                  </span>
                  <span v-else-if="item.data.before" class="text-danger ms-2">
                    Removed "{{ item.data.before }}"
                  </span>
                </div>
                <div v-else-if="item.type === 'creation'" class="fs-7 text-muted">
                  Quote was created and is now available in the system
                </div>
              </div>
              
              <!-- Edit Form -->
              <div v-else>
                <textarea
                  v-model="editCommentText"
                  class="form-control mb-2"
                  rows="3"
                ></textarea>
                <div class="d-flex justify-content-end gap-2">
                  <button
                    type="button"
                    class="btn btn-sm btn-light"
                    @click="cancelEdit"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm btn-primary"
                    @click="updateComment(item)"
                    :disabled="isSubmitting"
                  >
                    Update
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-5">
        <i class="fas fa-comments fs-3x text-muted mb-3"></i>
        <p class="text-muted">No updates or comments yet</p>
        <button
          v-if="!showAddComment"
          type="button"
          class="btn btn-sm btn-light-primary"
          @click="toggleAddComment"
        >
          Add the first comment
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import ApiService from '@/core/services/ApiService';
import Swal from 'sweetalert2';
import { formatDistanceToNow, parseISO } from 'date-fns';

interface Comment {
  id: string;
  content_type: number;
  content_type_name: string;
  object_id: string;
  text: string;
  created_on: string;
  created_by: string;
  created_by_username: string;
  created_by_name?: string;
  modified_on: string;
  modified_by?: string;
  status: string;
}

interface Modification {
  id: string;
  field: string;
  before?: string;
  after?: string;
  time: string;
  user_username?: string;
  modified_by_name?: string;
}

interface TimelineItem {
  id: string;
  type: 'comment' | 'modification' | 'creation';
  timestamp: string;
  user: string;
  data: Comment | Modification | any;
}

interface Props {
  quoteId: string;
  quoteData?: any;
}

const props = defineProps<Props>();

const comments = ref<Comment[]>([]);
const modifications = ref<Modification[]>([]);
const isLoading = ref(false);
const isSubmitting = ref(false);
const showAddComment = ref(false);
const newCommentText = ref('');
const editingCommentId = ref<string | null>(null);
const editCommentText = ref('');

// Quote content type ID (from Django ContentType)
const quoteContentTypeId = 22;

// Computed timeline items combining comments and modifications
const timelineItems = computed<TimelineItem[]>(() => {
  const items: TimelineItem[] = [];
  
  // Add creation event if quote data available
  if (props.quoteData?.created_on) {
    items.push({
      id: `creation-${props.quoteId}`,
      type: 'creation',
      timestamp: props.quoteData.created_on,
      user: props.quoteData.created_by_name || 
            props.quoteData.created_by_username || 
            'System',
      data: {
        field: '__created__',
        after: 'Quote created'
      }
    });
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
    items.push({
      id: mod.id,
      type: 'modification',
      timestamp: mod.time,
      user: mod.modified_by_name || mod.user_username || 'System',
      data: mod
    });
  });
  
  // Sort by timestamp (newest first)
  return items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
});

const getInitials = (name: string): string => {
  if (!name) return '?';
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

const getAvatarClass = (item: TimelineItem): string => {
  switch (item.type) {
    case 'comment': return 'bg-light-primary text-primary';
    case 'creation': return 'bg-light-success text-success';
    case 'modification': return 'bg-light-warning text-warning';
    default: return 'bg-light-secondary text-secondary';
  }
};

const getTimelineIcon = (item: TimelineItem): string => {
  switch (item.type) {
    case 'creation': return 'fas fa-plus';
    case 'modification': return 'fas fa-edit';
    default: return 'fas fa-info';
  }
};

const getActionText = (item: TimelineItem): string => {
  switch (item.type) {
    case 'comment': return 'commented';
    case 'creation': return 'created quote';
    case 'modification': 
      const mod = item.data as Modification;
      return `updated ${formatFieldName(mod.field)}`;
    default: return '';
  }
};

const formatFieldName = (fieldName: string): string => {
  if (fieldName === '__created__') return 'creation';
  if (fieldName === '__deleted__') return 'deletion';
  
  return fieldName
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const formatDate = (date: string): string => {
  if (!date) return '';
  try {
    return formatDistanceToNow(parseISO(date), { addSuffix: true });
  } catch {
    return 'Unknown time';
  }
};

const canEditComment = (item: TimelineItem): boolean => {
  // TODO: Check if current user is the comment author
  return item.type === 'comment';
};

const loadComments = async () => {
  try {
    const response = await ApiService.query('comments', {
      content_type: quoteContentTypeId,
      object_id: props.quoteId,
      ordering: '-created_on'
    });
    
    comments.value = response.data.results || response.data || [];
  } catch (error) {
    console.error('Error loading comments:', error);
    comments.value = [];
  }
};

const loadModifications = async () => {
  try {
    const response = await ApiService.get(`modifications/for_object/?model=Quote&object_id=${props.quoteId}`);
    modifications.value = response.data || [];
  } catch (error) {
    console.error('Error loading modifications:', error);
    modifications.value = [];
  }
};

const loadData = async () => {
  isLoading.value = true;
  try {
    await Promise.all([
      loadComments(),
      loadModifications()
    ]);
  } finally {
    isLoading.value = false;
  }
};

const toggleAddComment = () => {
  showAddComment.value = !showAddComment.value;
  if (showAddComment.value) {
    newCommentText.value = '';
  }
};

const cancelAddComment = () => {
  showAddComment.value = false;
  newCommentText.value = '';
};

const submitComment = async () => {
  if (!newCommentText.value.trim()) return;
  
  isSubmitting.value = true;
  try {
    const commentData = {
      content_type: quoteContentTypeId,
      object_id: props.quoteId,
      text: newCommentText.value.trim()
    };

    await ApiService.post('comments/', commentData);
    
    // Reset form
    newCommentText.value = '';
    showAddComment.value = false;
    
    // Reload data
    await loadData();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Comment added successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('Error submitting comment:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to add comment'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const editComment = (item: TimelineItem) => {
  if (item.type !== 'comment') return;
  editingCommentId.value = item.id;
  editCommentText.value = (item.data as Comment).text;
};

const cancelEdit = () => {
  editingCommentId.value = null;
  editCommentText.value = '';
};

const updateComment = async (item: TimelineItem) => {
  if (item.type !== 'comment') return;
  
  isSubmitting.value = true;
  try {
    await ApiService.patch(`comments/${item.id}/`, {
      text: editCommentText.value.trim()
    });
    
    // Reset editing state
    editingCommentId.value = null;
    editCommentText.value = '';
    
    // Reload data
    await loadData();
    
    Swal.fire({
      icon: 'success',
      title: 'Success',
      text: 'Comment updated successfully',
      timer: 2000,
      showConfirmButton: false
    });
  } catch (error) {
    console.error('Error updating comment:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Failed to update comment'
    });
  } finally {
    isSubmitting.value = false;
  }
};

const deleteComment = async (item: TimelineItem) => {
  if (item.type !== 'comment') return;
  
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Delete Comment?',
    text: 'This action cannot be undone',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    confirmButtonText: 'Yes, delete',
    cancelButtonText: 'Cancel'
  });

  if (result.isConfirmed) {
    try {
      await ApiService.delete(`comments/${item.id}/`);
      await loadData();
      
      Swal.fire({
        icon: 'success',
        title: 'Deleted',
        text: 'Comment has been deleted',
        timer: 2000,
        showConfirmButton: false
      });
    } catch (error) {
      console.error('Error deleting comment:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to delete comment'
      });
    }
  }
};

// Watch for quote ID changes
watch(() => props.quoteId, (newId) => {
  if (newId) {
    loadData();
  }
});

onMounted(() => {
  if (props.quoteId) {
    loadData();
  }
});
</script>

<style scoped>
.timeline-list {
  max-height: 500px;
  overflow-y: auto;
}

.bg-light-gray-100 {
  background-color: #f5f8fa;
}

.symbol-label {
  font-size: 12px;
}

.text-decoration-line-through {
  text-decoration: line-through;
}
</style>