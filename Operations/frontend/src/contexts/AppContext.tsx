import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

interface AppContextType {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  currentPage: string;
  setCurrentPage: (page: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider = ({ children }: AppProviderProps) => {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [currentPage, setCurrentPage] = useState<string>('dashboard');

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <AppContext.Provider value={{ sidebarOpen, toggleSidebar, currentPage, setCurrentPage }}>
      {children}
    </AppContext.Provider>
  );
};
