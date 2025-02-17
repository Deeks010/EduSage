
import React, { createContext, useState, useContext } from 'react';

const MouseEnterContext = createContext();

export const MouseEnterProvider = ({ children }) => {
  const [isMouseEntered, setIsMouseEntered] = useState(false);

  return (
    <MouseEnterContext.Provider value={[isMouseEntered, setIsMouseEntered]}>
      {children}
    </MouseEnterContext.Provider>
  );
};


export const useMouseEnter = () => {
  const context = useContext(MouseEnterContext);
  if (!context) {
    throw new Error('useMouseEnter must be used within a MouseEnterProvider');
  }
  return context;
};