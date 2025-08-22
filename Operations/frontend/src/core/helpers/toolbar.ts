import { onMounted, onUnmounted } from 'vue'
import { useToolbarStore, type ToolbarAction } from '@/stores/toolbar'

/**
 * Composable to manage toolbar actions for a specific page/component
 * Automatically clears actions when component is unmounted
 * 
 * Example usage in a page component:
 * 
 * ```typescript
 * import { useToolbar, createToolbarActions } from '@/core/helpers/toolbar'
 * 
 * export default defineComponent({
 *   setup() {
 *     const { setToolbarActions } = useToolbar()
 * 
 *     const openModal = () => {
 *       // Modal opening logic
 *     }
 * 
 *     onMounted(() => {
 *       setToolbarActions([
 *         createToolbarActions.primary('add-item', 'Add Item', openModal, 'plus'),
 *         createToolbarActions.secondary('export', 'Export', () => console.log('Export'), 'download')
 *       ])
 *     })
 *   }
 * })
 * ```
 */
export function useToolbar() {
  const toolbarStore = useToolbarStore()

  /**
   * Set toolbar actions for the current page
   * @param actions Array of toolbar actions to display
   */
  const setToolbarActions = (actions: ToolbarAction[]) => {
    toolbarStore.setActions(actions)
  }

  /**
   * Add a single toolbar action
   * @param action Toolbar action to add
   */
  const addToolbarAction = (action: ToolbarAction) => {
    toolbarStore.addAction(action)
  }

  /**
   * Remove a toolbar action by ID
   * @param actionId ID of the action to remove
   */
  const removeToolbarAction = (actionId: string) => {
    toolbarStore.removeAction(actionId)
  }

  /**
   * Clear all toolbar actions
   */
  const clearToolbarActions = () => {
    toolbarStore.clearActions()
  }

  // Automatically clear toolbar actions when component is unmounted
  onUnmounted(() => {
    clearToolbarActions()
  })

  return {
    setToolbarActions,
    addToolbarAction,
    removeToolbarAction,
    clearToolbarActions
  }
}

/**
 * Helper function to create common toolbar action types
 */
export const createToolbarActions = {
  /**
   * Create a primary button action
   */
  primary: (id: string, label: string, handler: () => void, icon?: string): ToolbarAction => ({
    id,
    label,
    variant: 'primary',
    icon,
    handler
  }),

  /**
   * Create a secondary button action
   */
  secondary: (id: string, label: string, handler: () => void, icon?: string): ToolbarAction => ({
    id,
    label,
    variant: 'secondary',
    icon,
    handler
  }),

  /**
   * Create a modal trigger action
   */
  modal: (id: string, label: string, modalTarget: string, variant: 'primary' | 'secondary' = 'primary', icon?: string): ToolbarAction => ({
    id,
    label,
    variant,
    icon,
    modalTarget,
    handler: () => {} // No-op for modal triggers
  }),

  /**
   * Create a link action
   */
  link: (id: string, label: string, href: string, variant: 'primary' | 'secondary' = 'primary', icon?: string): ToolbarAction => ({
    id,
    label,
    variant,
    icon,
    href,
    handler: () => {} // No-op for links
  })
}