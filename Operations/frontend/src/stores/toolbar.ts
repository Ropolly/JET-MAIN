import { defineStore } from 'pinia'
import { ref, type Ref } from 'vue'

export interface DropdownItem {
  id?: string
  label?: string
  icon?: string
  handler?: () => void
  className?: string
  divider?: boolean
}

export interface ToolbarAction {
  id: string
  label: string
  variant?: 'primary' | 'secondary' | 'success' | 'info' | 'warning' | 'danger' | 'dark'
  icon?: string
  handler?: () => void
  modalTarget?: string
  href?: string
  disabled?: boolean
  isDropdown?: boolean
  dropdownItems?: DropdownItem[]
}

export const useToolbarStore = defineStore('toolbar', () => {
  const actions: Ref<ToolbarAction[]> = ref([])

  const setActions = (newActions: ToolbarAction[]) => {
    actions.value = newActions
  }

  const addAction = (action: ToolbarAction) => {
    actions.value.push(action)
  }

  const removeAction = (actionId: string) => {
    actions.value = actions.value.filter(action => action.id !== actionId)
  }

  const clearActions = () => {
    actions.value = []
  }

  return {
    actions,
    setActions,
    addAction,
    removeAction,
    clearActions
  }
})