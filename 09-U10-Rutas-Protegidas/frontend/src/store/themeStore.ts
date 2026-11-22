import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface ThemeState {
  darkMode: boolean
  toggleTheme: () => void
}

function applyTheme(darkMode: boolean) {
  document.documentElement.classList.toggle('dark', darkMode)
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      darkMode: false,
      toggleTheme: () => {
        const darkMode = !get().darkMode
        applyTheme(darkMode)
        set({ darkMode })
      },
    }),
    {
      name: 'theme-storage',
      onRehydrateStorage: () => (state) => applyTheme(state?.darkMode ?? false),
    },
  ),
)

export function initializeTheme() {
  applyTheme(useThemeStore.getState().darkMode)
}
