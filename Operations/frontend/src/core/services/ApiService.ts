import type { App } from "vue";
import type { AxiosResponse, AxiosRequestConfig } from "axios";
import axios from "axios";
import VueAxios from "vue-axios";
import JwtService from "@/core/services/JwtService";

/**
 * @description service to call HTTP request via Axios
 */
class ApiService {
  /**
   * @description property to share vue instance
   */
  public static vueInstance: App;

  /**
   * @description initialize vue axios
   */
  public static init(app: App<Element>) {
    ApiService.vueInstance = app;
    ApiService.vueInstance.use(VueAxios, axios);
    
    // Set base URL from environment or default to Django backend
    ApiService.vueInstance.axios.defaults.baseURL =
      import.meta.env.VITE_APP_API_URL || "http://localhost:8001/api";
    
    // Set default headers
    ApiService.vueInstance.axios.defaults.headers.common["Accept"] = "application/json";
    ApiService.vueInstance.axios.defaults.headers.common["Content-Type"] = "application/json";
    
    // Setup interceptors
    ApiService.setupInterceptors();
  }

  /**
   * @description setup axios interceptors
   */
  private static setupInterceptors(): void {
    // Request interceptor
    ApiService.vueInstance.axios.interceptors.request.use(
      (config: AxiosRequestConfig) => {
        // Add auth token to requests if available
        const token = JwtService.getToken();
        if (token) {
          config.headers = config.headers || {};
          config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    ApiService.vueInstance.axios.interceptors.response.use(
      (response: AxiosResponse) => {
        return response;
      },
      async (error) => {
        // Handle 401 Unauthorized errors
        if (error.response?.status === 401) {
          const authStore = (await import("@/stores/auth")).useAuthStore();
          
          // Try to refresh token if we have a refresh token
          const refreshToken = localStorage.getItem("refresh_token");
          if (refreshToken && !error.config._retry) {
            error.config._retry = true;
            
            try {
              await authStore.refreshToken();
              // Retry the original request with new token
              return ApiService.vueInstance.axios(error.config);
            } catch (refreshError) {
              // Refresh failed, logout user
              authStore.logout();
              
              // Redirect to login page
              if (window.location.pathname !== "/sign-in") {
                window.location.href = "/sign-in";
              }
            }
          } else {
            // No refresh token or refresh already failed
            authStore.logout();
            
            // Redirect to login page
            if (window.location.pathname !== "/sign-in") {
              window.location.href = "/sign-in";
            }
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  /**
   * @description set the default HTTP request headers
   */
  public static setHeader(): void {
    const token = JwtService.getToken();
    if (token) {
      ApiService.vueInstance.axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }
  }

  /**
   * @description remove default HTTP request headers
   */
  public static removeHeader(): void {
    delete ApiService.vueInstance.axios.defaults.headers.common["Authorization"];
  }

  /**
   * @description send the GET HTTP request
   * @param resource: string
   * @param params: AxiosRequestConfig
   * @returns Promise<AxiosResponse>
   */
  public static query(resource: string, params: any): Promise<AxiosResponse> {
    // Ensure trailing slash is before query parameters, not after
    let url = resource;
    const queryIndex = url.indexOf('?');
    if (queryIndex > 0) {
      // URL has query parameters - insert slash before them
      const path = url.substring(0, queryIndex);
      const query = url.substring(queryIndex);
      url = path.endsWith('/') ? resource : `${path}/${query}`;
    } else {
      // No query parameters - just append slash if needed
      url = url.endsWith('/') ? url : `${url}/`;
    }
    return ApiService.vueInstance.axios.get(url, { params });
  }

  /**
   * @description send the GET HTTP request
   * @param resource: string
   * @param slug: string
   * @returns Promise<AxiosResponse>
   */
  public static get(
    resource: string,
    slug = "" as string
  ): Promise<AxiosResponse> {
    let url = slug ? `${resource}/${slug}` : resource;

    // Ensure trailing slash is before query parameters, not after
    const queryIndex = url.indexOf('?');
    if (queryIndex > 0) {
      // URL has query parameters - insert slash before them
      const path = url.substring(0, queryIndex);
      const query = url.substring(queryIndex);
      url = path.endsWith('/') ? url : `${path}/${query}`;
    } else {
      // No query parameters - just append slash if needed
      url = url.endsWith('/') ? url : `${url}/`;
    }

    return ApiService.vueInstance.axios.get(url);
  }

  /**
   * @description set the POST HTTP request
   * @param resource: string
   * @param params: AxiosRequestConfig
   * @returns Promise<AxiosResponse>
   */
  public static post(resource: string, params: any): Promise<AxiosResponse> {
    const url = resource.endsWith('/') ? resource : `${resource}/`;
    return ApiService.vueInstance.axios.post(url, params);
  }

  /**
   * @description send the UPDATE HTTP request
   * @param resource: string
   * @param slug: string
   * @param params: AxiosRequestConfig
   * @returns Promise<AxiosResponse>
   */
  public static update(
    resource: string,
    slug: string,
    params: any
  ): Promise<AxiosResponse> {
    let url = `${resource}/${slug}`;
    url = url.endsWith('/') ? url : `${url}/`;
    return ApiService.vueInstance.axios.put(url, params);
  }

  /**
   * @description Send the PUT HTTP request
   * @param resource: string
   * @param params: AxiosRequestConfig
   * @returns Promise<AxiosResponse>
   */
  public static put(resource: string, params: any): Promise<AxiosResponse> {
    const url = resource.endsWith('/') ? resource : `${resource}/`;
    return ApiService.vueInstance.axios.put(url, params);
  }

  /**
   * @description Send the PATCH HTTP request
   * @param resource: string
   * @param params: AxiosRequestConfig
   * @returns Promise<AxiosResponse>
   */
  public static patch(resource: string, params: any): Promise<AxiosResponse> {
    const url = resource.endsWith('/') ? resource : `${resource}/`;
    return ApiService.vueInstance.axios.patch(url, params);
  }

  /**
   * @description Send the DELETE HTTP request
   * @param resource: string
   * @returns Promise<AxiosResponse>
   */
  public static delete(resource: string): Promise<AxiosResponse> {
    const url = resource.endsWith('/') ? resource : `${resource}/`;
    return ApiService.vueInstance.axios.delete(url);
  }

  /**
   * @description Upload files using FormData
   * @param resource: string
   * @param formData: FormData
   * @returns Promise<AxiosResponse>
   */
  public static upload(resource: string, formData: FormData): Promise<AxiosResponse> {
    const url = resource.endsWith('/') ? resource : `${resource}/`;
    return ApiService.vueInstance.axios.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }
}

export default ApiService;