import { ref } from "vue";
import { defineStore } from "pinia";
import ApiService from "@/core/services/ApiService";
import JwtService from "@/core/services/JwtService";

export interface User {
  id?: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  mfa_enabled?: boolean;
  phone_verified?: boolean;
  phone?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
  sms_code?: string;
}

export interface MfaResponse {
  mfa_required: boolean;
  phone_number?: string;
  message?: string;
}

export interface SmsCodeResult {
  success: boolean;
  message?: string;
  phone_number?: string;
  expires_at?: string;
  error?: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export const useAuthStore = defineStore("auth", () => {
  const errors = ref<Record<string, any>>({});
  const user = ref<User | null>(null);
  const isAuthenticated = ref(!!JwtService.getToken());

  /**
   * Set authentication data
   */
  function setAuth(authUser: User) {
    isAuthenticated.value = true;
    user.value = authUser;
    errors.value = {};
  }

  /**
   * Set error messages
   */
  function setError(error: any) {
    errors.value = { ...error };
  }

  /**
   * Clear authentication data
   */
  function purgeAuth() {
    isAuthenticated.value = false;
    user.value = null;
    errors.value = {};
    JwtService.destroyToken();
    localStorage.removeItem("refresh_token");
  }

  /**
   * Login with username and password (with MFA support)
   */
  async function login(credentials: LoginCredentials) {
    try {
      errors.value = {};

      // Try MFA login first
      const { data } = await ApiService.post("/auth/login-with-mfa/", {
        username: credentials.username.trim(),
        password: credentials.password.trim(),
        sms_code: credentials.sms_code,
      });

      // Check if MFA is required
      if (data.mfa_required) {
        return {
          mfa_required: true,
          phone_number: data.phone_number,
          message: data.message
        };
      }

      // Save tokens
      JwtService.saveToken(data.access);
      if (data.refresh) {
        localStorage.setItem("refresh_token", data.refresh);
      }

      // Set auth header for future requests
      ApiService.setHeader();

      // Set user data
      if (data.user) {
        setAuth(data.user);
      }

      return data;
    } catch (error: any) {
      const message = error.response?.data?.error ||
                     error.response?.data?.detail ||
                     "Invalid credentials";
      setError({ general: message });
      throw error;
    }
  }

  /**
   * Register a new user
   */
  async function register(userData: RegisterData) {
    try {
      errors.value = {};
      
      // Create user profile directly since registration endpoint doesn't exist
      const { data } = await ApiService.post("/users/", {
        user_id: null, // Will need to create user first
        first_name: userData.first_name || '',
        last_name: userData.last_name || '',
        email: userData.email,
        status: 'active'
      });
      
      // Note: This is a simplified approach. In a real implementation,
      // you would need backend support for user registration
      setError({ general: "Registration endpoint not implemented. Please contact administrator." });
      throw new Error("Registration not implemented");
      
    } catch (error: any) {
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     "Registration not available";
      
      setError({ general: message });
      throw error;
    }
  }

  /**
   * Get current user profile
   */
  async function getUserProfile() {
    try {
      const { data } = await ApiService.get("/users/me/");
      setAuth(data);
      return data;
    } catch (error) {
      console.error("Failed to get user profile:", error);
      // If we can't get the profile, the token might be invalid
      purgeAuth();
      throw error;
    }
  }

  /**
   * Logout user
   */
  function logout() {
    purgeAuth();
  }

  /**
   * Verify authentication on app load
   */
  async function verifyAuth() {
    const token = JwtService.getToken();
    
    if (!token) {
      purgeAuth();
      return false;
    }

    try {
      // Set auth header
      ApiService.setHeader();
      
      // Verify token with backend
      await ApiService.post("/token/verify/", { token });
      
      // Get user profile
      await getUserProfile();
      
      return true;
    } catch (error) {
      // Token is invalid or expired
      purgeAuth();
      return false;
    }
  }

  /**
   * Refresh access token using refresh token
   */
  async function refreshToken() {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      
      if (!refreshToken) {
        throw new Error("No refresh token available");
      }
      
      const { data } = await ApiService.post("/token/refresh/", {
        refresh: refreshToken,
      });
      
      // Save new access token
      JwtService.saveToken(data.access);
      
      // Update auth header
      ApiService.setHeader();
      
      return data;
    } catch (error) {
      // If refresh fails, logout user
      purgeAuth();
      throw error;
    }
  }

  /**
   * Update user profile
   */
  async function updateProfile(profileData: Partial<User>) {
    try {
      // Since there's no PUT /users/me/, we need to use the regular PUT endpoint with user ID
      if (!user.value?.id) {
        throw new Error("User profile not loaded");
      }
      
      // Transform data to match UserProfileWriteSerializer format
      const transformedData = {
        first_name: profileData.first_name,
        last_name: profileData.last_name,
        email: profileData.email,
        phone: profileData.phone,
        // Add other fields as needed
      };
      
      const { data } = await ApiService.put(`/users/${user.value.id}/`, transformedData);
      setAuth(data);
      return data;
    } catch (error: any) {
      const message = error.response?.data?.detail || "Failed to update profile";
      setError({ general: message });
      throw error;
    }
  }

  /**
   * Change password
   */
  async function changePassword(oldPassword: string, newPassword: string) {
    try {
      // Password change endpoint doesn't exist in current backend
      setError({ general: "Password change endpoint not implemented. Please contact administrator." });
      throw new Error("Password change not implemented");
    } catch (error: any) {
      const message = "Password change functionality not available";
      setError({ general: message });
      throw error;
    }
  }

  /**
   * Request password reset
   */
  async function forgotPassword(email: string) {
    try {
      // Password reset endpoint doesn't exist in current backend
      setError({ general: "Password reset endpoint not implemented. Please contact administrator." });
      throw new Error("Password reset not implemented");
    } catch (error: any) {
      const message = "Password reset functionality not available";
      setError({ general: message });
      throw error;
    }
  }

  /**
   * Send SMS verification code
   */
  async function sendSmsCode(phoneNumber: string): Promise<SmsCodeResult> {
    try {
      const { data } = await ApiService.post("/auth/send-sms-code/", {
        phone_number: phoneNumber,
      });

      return {
        success: true,
        message: data.message,
        phone_number: data.phone_number,
        expires_at: data.expires_at,
      };
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || "Failed to send SMS code";
      setError({ sms: errorMessage });
      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  /**
   * Verify SMS code
   */
  async function verifySmsCode(phoneNumber: string, code: string): Promise<SmsCodeResult> {
    try {
      const { data } = await ApiService.post("/auth/verify-sms-code/", {
        phone_number: phoneNumber,
        code: code,
      });

      return {
        success: true,
        message: data.message,
        phone_number: data.phone_number,
      };
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || "Failed to verify SMS code";
      setError({ sms: errorMessage });
      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  /**
   * Setup phone number for authenticated user
   */
  async function setupPhone(phoneNumber: string, code?: string): Promise<SmsCodeResult> {
    try {
      const payload: any = { phone_number: phoneNumber };
      if (code) {
        payload.code = code;
      }

      const { data } = await ApiService.post("/auth/setup-phone/", payload);

      // If phone was verified and saved, update user data
      if (data.phone_verified && user.value) {
        user.value = {
          ...user.value,
          phone: data.phone_number,
          phone_verified: true,
        };
      }

      return {
        success: true,
        message: data.message,
        phone_number: data.phone_number,
        expires_at: data.expires_at,
      };
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || "Failed to setup phone";
      setError({ phone: errorMessage });
      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  /**
   * Enable or disable MFA for current user
   */
  async function updateMfaSettings(enabled: boolean) {
    try {
      if (!user.value?.id) {
        throw new Error("User not authenticated");
      }

      // Update user profile with MFA setting
      const { data } = await ApiService.put(`/users/${user.value.id}/`, {
        mfa_enabled: enabled,
      });

      // Update local user data
      if (user.value) {
        user.value = { ...user.value, mfa_enabled: enabled };
      }

      return data;
    } catch (error: any) {
      const message = error.response?.data?.detail || "Failed to update MFA settings";
      setError({ mfa: message });
      throw error;
    }
  }

  return {
    errors,
    user,
    isAuthenticated,
    setAuth,
    setError,
    purgeAuth,
    login,
    register,
    logout,
    verifyAuth,
    getUserProfile,
    updateProfile,
    changePassword,
    forgotPassword,
    refreshToken,
    // MFA methods
    sendSmsCode,
    verifySmsCode,
    setupPhone,
    updateMfaSettings,
  };
});