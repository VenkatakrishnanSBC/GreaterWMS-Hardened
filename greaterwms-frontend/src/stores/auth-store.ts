import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AuthState {
    openid: string;
    loginName: string;
    loginId: number;
    isAuthenticated: boolean;
    staffType: string;
    warehouseName: string;

    login: (data: {
        openid: string;
        loginName: string;
        loginId: number;
        staffType?: string;
    }) => void;
    logout: () => void;
    setWarehouse: (name: string) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            openid: "",
            loginName: "",
            loginId: 0,
            isAuthenticated: false,
            staffType: "",
            warehouseName: "",

            login: (data) =>
                set({
                    openid: data.openid,
                    loginName: data.loginName,
                    loginId: data.loginId,
                    staffType: data.staffType || "",
                    isAuthenticated: true,
                }),

            logout: () =>
                set({
                    openid: "",
                    loginName: "",
                    loginId: 0,
                    isAuthenticated: false,
                    staffType: "",
                }),

            setWarehouse: (name) => set({ warehouseName: name }),
        }),
        { name: "gwms-auth" }
    )
);
