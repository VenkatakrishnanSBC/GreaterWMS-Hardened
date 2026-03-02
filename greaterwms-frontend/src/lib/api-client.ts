const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

interface RequestOptions extends RequestInit {
    params?: Record<string, string>;
}

interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

async function request<T>(
    endpoint: string,
    options: RequestOptions = {}
): Promise<T> {
    const { params, headers: customHeaders, ...rest } = options;

    let url = `${API_BASE}/${endpoint}`;
    if (params) {
        const searchParams = new URLSearchParams(params);
        url += `?${searchParams.toString()}`;
    }

    const token =
        typeof window !== "undefined" ? localStorage.getItem("openid") : null;
    const operator =
        typeof window !== "undefined" ? localStorage.getItem("login_id") : null;
    const language =
        typeof window !== "undefined"
            ? localStorage.getItem("lang") || "en-US"
            : "en-US";

    const headers: Record<string, string> = {
        "Content-Type": "application/json",
        language,
        ...(customHeaders as Record<string, string>),
    };

    if (token) headers.token = token;
    if (operator) headers.operator = operator;

    const response = await fetch(url, { headers, ...rest });

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw {
            status: response.status,
            detail: error.detail || `HTTP ${response.status}`,
            data: error,
        };
    }

    return response.json();
}

export const api = {
    get: <T>(endpoint: string, params?: Record<string, string>) =>
        request<T>(endpoint, { method: "GET", params }),

    post: <T>(endpoint: string, data?: unknown) =>
        request<T>(endpoint, { method: "POST", body: JSON.stringify(data) }),

    put: <T>(endpoint: string, data?: unknown) =>
        request<T>(endpoint, { method: "PUT", body: JSON.stringify(data) }),

    patch: <T>(endpoint: string, data?: unknown) =>
        request<T>(endpoint, { method: "PATCH", body: JSON.stringify(data) }),

    delete: <T>(endpoint: string) =>
        request<T>(endpoint, { method: "DELETE" }),

    paginated: <T>(endpoint: string, page = 1, pageSize = 30) =>
        request<PaginatedResponse<T>>(endpoint, {
            method: "GET",
            params: { page: String(page), max_page: String(pageSize) },
        }),
};

export type { PaginatedResponse };
