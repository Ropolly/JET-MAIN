import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

// Define available color palettes
export interface ColorPalette {
  id: string;
  name: string;
  colors: {
    bgPrimary: string;
    bgSecondary: string;
    textPrimary: string;
    textSecondary: string;
    accentPrimary: string;
    accentSecondary: string;
    buttonPrimary: string;
    buttonText: string;
    stroke: string;
    tertiary: string;
  };
}

// Predefined color palettes
export const colorPalettes: ColorPalette[] = [
  {
    id: 'palette-13',
    name: 'Ocean Blue',
    colors: {
      bgPrimary: '#fffffe',
      bgSecondary: '#f2f4f6',
      textPrimary: '#00214d',
      textSecondary: '#1b2d45',
      accentPrimary: '#00ebc7',
      accentSecondary: '#ff5470',
      buttonPrimary: '#00ebc7',
      buttonText: '#00214d',
      stroke: '#00214d',
      tertiary: '#fde24f'
    }
  },
  {
    id: 'palette-4',
    name: 'Forest Green',
    colors: {
      bgPrimary: '#fffffe',
      bgSecondary: '#f0f0f0',
      textPrimary: '#272343',
      textSecondary: '#2d334a',
      accentPrimary: '#bae8e8',
      accentSecondary: '#e3f6f5',
      buttonPrimary: '#ffd803',
      buttonText: '#272343',
      stroke: '#272343',
      tertiary: '#bae8e8'
    }
  },
  {
    id: 'palette-11',
    name: 'Sunset Orange',
    colors: {
      bgPrimary: '#fffffe',
      bgSecondary: '#f9f4ef',
      textPrimary: '#020826',
      textSecondary: '#716040',
      accentPrimary: '#8c7851',
      accentSecondary: '#f25042',
      buttonPrimary: '#f25042',
      buttonText: '#fffffe',
      stroke: '#020826',
      tertiary: '#eaddcf'
    }
  },
  {
    id: 'palette-17',
    name: 'Purple Dream',
    colors: {
      bgPrimary: '#fffffe',
      bgSecondary: '#f5f5f5',
      textPrimary: '#2b2c34',
      textSecondary: '#2b2c34',
      accentPrimary: '#6246ea',
      accentSecondary: '#d1d1e9',
      buttonPrimary: '#6246ea',
      buttonText: '#fffffe',
      stroke: '#2b2c34',
      tertiary: '#e45858'
    }
  }
];

interface ThemeContextType {
  currentPalette: ColorPalette;
  setPalette: (paletteId: string) => void;
  availablePalettes: ColorPalette[];
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

interface ThemeProviderProps {
  children: ReactNode;
}

export const ThemeProvider = ({ children }: ThemeProviderProps) => {
  // Get saved palette from localStorage or use default
  const [currentPalette, setCurrentPalette] = useState<ColorPalette>(() => {
    const savedPaletteId = localStorage.getItem('colorPalette');
    return colorPalettes.find(palette => palette.id === savedPaletteId) || colorPalettes[0];
  });

  // Apply palette to CSS variables
  useEffect(() => {
    const root = document.documentElement;
    Object.entries(currentPalette.colors).forEach(([key, value]) => {
      // Convert camelCase to kebab-case for CSS variables
      const cssVarName = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      root.style.setProperty(`--${cssVarName}`, value);
    });
    
    // Save selection to localStorage
    localStorage.setItem('colorPalette', currentPalette.id);
  }, [currentPalette]);

  const setPalette = (paletteId: string) => {
    const newPalette = colorPalettes.find(palette => palette.id === paletteId);
    if (newPalette) {
      setCurrentPalette(newPalette);
    }
  };

  return (
    <ThemeContext.Provider value={{ 
      currentPalette, 
      setPalette, 
      availablePalettes: colorPalettes 
    }}>
      {children}
    </ThemeContext.Provider>
  );
};
