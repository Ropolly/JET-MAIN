<template>
  <div class="d-flex flex-column flex-lg-row">
    <!--begin::Content-->
    <div class="flex-lg-row-fluid me-lg-7 me-xl-10">
      <!--begin::Form-->
      <form
        @submit.prevent="handleSubmit"
        id="email-template-form"
        class="form"
        novalidate="novalidate"
      >
        <!--begin::Card-->
        <div class="card card-flush py-4">
          <!--begin::Card header-->
          <div class="card-header">
            <div class="card-title">
              <h2>{{ isEditing ? 'Edit Email Template' : 'Create Email Template' }}</h2>
            </div>
          </div>
          <!--end::Card header-->

          <!--begin::Card body-->
          <div class="card-body pt-0">
            <div class="row">
              <!--begin::Title-->
              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="required form-label">Template Title</label>
                  <input
                    type="text"
                    v-model="formData.title"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.title}"
                    placeholder="Enter template title"
                    required
                  />
                  <div v-if="errors.title" class="invalid-feedback">
                    {{ errors.title }}
                  </div>
                </div>
              </div>

              <!--begin::Category-->
              <div class="col-xl-6">
                <div class="mb-10">
                  <label class="required form-label">Category</label>
                  <select
                    v-model="formData.category"
                    class="form-select mb-2"
                    :class="{'is-invalid': errors.category}"
                    required
                  >
                    <option value="">Select category</option>
                    <option value="general">General</option>
                    <option value="trip">Trip</option>
                    <option value="quote">Quote</option>
                    <option value="patient">Patient</option>
                    <option value="notification">Notification</option>
                  </select>
                  <div v-if="errors.category" class="invalid-feedback">
                    {{ errors.category }}
                  </div>
                </div>
              </div>

              <!--begin::Subject-->
              <div class="col-12">
                <div class="mb-10">
                  <label class="form-label">Email Subject</label>
                  <input
                    type="text"
                    v-model="formData.subject"
                    class="form-control mb-2"
                    :class="{'is-invalid': errors.subject}"
                    placeholder="Enter email subject"
                  />
                  <div v-if="errors.subject" class="invalid-feedback">
                    {{ errors.subject }}
                  </div>
                </div>
              </div>

              <!--begin::Content (WYSIWYG Editor)-->
              <div class="col-12">
                <div class="mb-10">
                  <label class="required form-label">Email Content</label>
                  <div class="card">
                    <div class="card-header">
                      <div class="card-title">
                        <span class="text-muted fs-7">
                          Use HTML for formatting. Available variables: &#123;&#123;patient_name&#125;&#125;, &#123;&#123;trip_number&#125;&#125;, &#123;&#123;quote_amount&#125;&#125;, etc.
                        </span>
                      </div>
                    </div>
                    <div class="card-body p-0">
                      <textarea
                        v-model="formData.content"
                        class="form-control border-0 rounded-0"
                        :class="{'is-invalid': errors.content}"
                        rows="15"
                        placeholder="Enter email content with HTML formatting..."
                        style="resize: vertical; min-height: 300px;"
                        required
                      ></textarea>
                    </div>
                  </div>
                  <div v-if="errors.content" class="invalid-feedback">
                    {{ errors.content }}
                  </div>
                </div>
              </div>

              <!--begin::Variables-->
              <div class="col-12">
                <div class="mb-10">
                  <label class="form-label">Template Variables</label>
                  <div class="card">
                    <div class="card-body">
                      <div class="row">
                        <div class="col-lg-6">
                          <div class="mb-5">
                            <input
                              v-model="newVariable"
                              type="text"
                              class="form-control"
                              placeholder="Add variable (e.g., patient_name)"
                              @keyup.enter="addVariable"
                            />
                          </div>
                        </div>
                        <div class="col-lg-6">
                          <button
                            type="button"
                            class="btn btn-light-primary"
                            @click="addVariable"
                          >
                            <KTIcon icon-name="plus" icon-class="fs-6 me-1" />
                            Add Variable
                          </button>
                        </div>
                      </div>
                      <div class="d-flex flex-wrap">
                        <span
                          v-for="(variable, index) in formData.variables"
                          :key="index"
                          class="badge badge-light-info me-2 mb-2"
                        >
                          {{ variable }}
                          <button
                            type="button"
                            class="btn btn-sm btn-icon btn-active-light-danger ms-2 p-0"
                            @click="removeVariable(index)"
                            style="width: 20px; height: 20px;"
                          >
                            <KTIcon icon-name="cross" icon-class="fs-8" />
                          </button>
                        </span>
                        <span v-if="formData.variables.length === 0" class="text-muted">
                          No variables added yet
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!--begin::Status-->
              <div class="col-12">
                <div class="mb-10">
                  <div class="form-check form-switch">
                    <input
                      v-model="formData.is_published"
                      class="form-check-input"
                      type="checkbox"
                      id="publishSwitch"
                    />
                    <label class="form-check-label fw-semibold" for="publishSwitch">
                      Publish Template
                    </label>
                    <div class="text-muted fs-7 mt-1">
                      Published templates are available for use in the system
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!--end::Card body-->

          <!--begin::Card footer-->
          <div class="card-footer d-flex justify-content-end py-6 px-9">
            <button
              type="button"
              class="btn btn-light me-2"
              @click="handleCancel"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ isEditing ? 'Update Template' : 'Create Template' }}
            </button>
          </div>
          <!--end::Card footer-->
        </div>
        <!--end::Card-->
      </form>
      <!--end::Form-->
    </div>
    <!--end::Content-->

    <!--begin::Sidebar-->
    <div class="flex-lg-row-auto w-lg-300px">
      <!--begin::Preview Card-->
      <div class="card card-flush py-4">
        <div class="card-header">
          <div class="card-title">
            <h3>Preview</h3>
          </div>
        </div>
        <div class="card-body">
          <div class="mb-5">
            <label class="form-label fw-bold">Subject:</label>
            <div class="text-gray-700">
              {{ formData.subject || 'No subject' }}
            </div>
          </div>
          <div class="mb-5">
            <label class="form-label fw-bold">Content Preview:</label>
            <div
              class="border rounded p-3"
              style="max-height: 400px; overflow-y: auto; background-color: #f9f9f9;"
              v-html="previewContent"
            ></div>
          </div>
          <div>
            <label class="form-label fw-bold">Status:</label>
            <div>
              <span :class="`badge badge-light-${formData.is_published ? 'success' : 'warning'}`">
                {{ formData.is_published ? 'Published' : 'Draft' }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <!--end::Preview Card-->
    </div>
    <!--end::Sidebar-->
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";

interface EmailTemplate {
  id?: string;
  title: string;
  subject: string;
  content: string;
  category: string;
  is_published: boolean;
  variables: string[];
}

export default defineComponent({
  name: "email-template-editor",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const loading = ref(false);
    const isEditing = ref(false);
    const templateId = ref<string | null>(null);
    const newVariable = ref("");
    const { setToolbarActions } = useToolbar();

    const formData = ref<EmailTemplate>({
      title: "",
      subject: "",
      content: "",
      category: "",
      is_published: false,
      variables: [],
    });

    const errors = ref<Record<string, string>>({});

    const previewContent = computed(() => {
      if (!formData.value.content) return "No content";

      // Simple preview - replace variables with sample data
      let preview = formData.value.content;

      // Only process variables that exist in the array
      if (formData.value.variables && formData.value.variables.length > 0) {
        formData.value.variables.forEach(variable => {
          const sampleValue = getSampleValue(variable);
          preview = preview.replace(new RegExp(`\\{\\{${variable}\\}\\}`, 'g'), sampleValue);
        });
      }

      return preview;
    });

    const getSampleValue = (variable: string): string => {
      const samples: Record<string, string> = {
        patient_name: "John Doe",
        trip_number: "TRIP-001",
        quote_amount: "$5,000",
        departure_date: "2024-01-15",
        pickup_location: "Tampa, FL",
        destination: "Miami, FL",
      };
      return samples[variable] || `[${variable}]`;
    };

    const initializeToolbar = () => {
      // Setup toolbar actions with proper function syntax
      setToolbarActions([
        {
          id: 'back-to-templates',
          label: 'Back to Templates',
          icon: 'arrow-left',
          variant: 'light',
          onClick: () => router.push({ name: "email-templates" })
        }
      ]);
    };

    const fetchTemplate = async () => {
      if (!templateId.value) return;

      loading.value = true;
      try {
        const response = await ApiService.get("email-templates", templateId.value);
        formData.value = {
          id: response.data.id,
          title: response.data.title || "",
          subject: response.data.subject || "",
          content: response.data.content || "",
          category: response.data.category || "",
          is_published: response.data.is_published || false,
          variables: response.data.variables || [],
        };
      } catch (error) {
        console.error("Error fetching template:", error);
        Swal.fire({
          title: "Error",
          text: "Failed to fetch email template",
          icon: "error",
        });
        router.push({ name: "email-templates" });
      } finally {
        loading.value = false;
      }
    };

    const validateForm = (): boolean => {
      errors.value = {};
      let isValid = true;

      if (!formData.value.title.trim()) {
        errors.value.title = "Title is required";
        isValid = false;
      }

      if (!formData.value.category) {
        errors.value.category = "Category is required";
        isValid = false;
      }

      if (!formData.value.content.trim()) {
        errors.value.content = "Content is required";
        isValid = false;
      }

      return isValid;
    };

    const handleSubmit = async () => {
      if (!validateForm()) return;

      loading.value = true;
      try {
        const payload = {
          title: formData.value.title,
          subject: formData.value.subject,
          content: formData.value.content,
          category: formData.value.category,
          is_published: formData.value.is_published,
          variables: formData.value.variables,
        };

        if (isEditing.value && templateId.value) {
          await ApiService.update("email-templates", templateId.value, payload);
          Swal.fire({
            title: "Success",
            text: "Email template updated successfully",
            icon: "success",
          });
        } else {
          await ApiService.post("email-templates", payload);
          Swal.fire({
            title: "Success",
            text: "Email template created successfully",
            icon: "success",
          });
        }

        router.push({ name: "email-templates" });
      } catch (error: any) {
        console.error("Error saving template:", error);

        if (error.response?.data) {
          const errorData = error.response.data;
          if (typeof errorData === 'object') {
            errors.value = errorData;
          }
        }

        Swal.fire({
          title: "Error",
          text: "Failed to save email template",
          icon: "error",
        });
      } finally {
        loading.value = false;
      }
    };

    const handleCancel = () => {
      router.push({ name: "email-templates" });
    };

    const addVariable = () => {
      const variable = newVariable.value.trim();
      if (variable && !formData.value.variables.includes(variable)) {
        formData.value.variables.push(variable);
        newVariable.value = "";
      }
    };

    const removeVariable = (index: number) => {
      formData.value.variables.splice(index, 1);
    };

    onMounted(() => {
      templateId.value = route.params.id as string || null;
      isEditing.value = !!templateId.value;

      initializeToolbar();

      if (isEditing.value) {
        fetchTemplate();
      }
    });

    return {
      loading,
      isEditing,
      formData,
      errors,
      newVariable,
      previewContent,
      handleSubmit,
      handleCancel,
      addVariable,
      removeVariable,
    };
  },
});
</script>

<style scoped>
.card-body textarea {
  font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
}

.preview-content {
  word-wrap: break-word;
  line-height: 1.5;
}
</style>