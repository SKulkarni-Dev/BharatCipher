import { createContext, useContext, useState, useMemo } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [investigator, setInvestigator] = useState(() => {
    const cached = sessionStorage.getItem('sih_investigator');
    return cached ? JSON.parse(cached) : null;
  });

  const value = useMemo(
    () => ({
      investigator,
      isAuthenticated: !!investigator,
      login: (inv) => {
        setInvestigator(inv);
        sessionStorage.setItem('sih_investigator', JSON.stringify(inv));
      },
      logout: () => {
        setInvestigator(null);
        sessionStorage.removeItem('sih_investigator');
      },
    }),
    [investigator]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
