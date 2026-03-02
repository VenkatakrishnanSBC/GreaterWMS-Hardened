"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, type PaginatedResponse } from "@/lib/api-client";
import { useState, useCallback } from "react";
import { toast } from "sonner";

interface UseCrudOptions {
    endpoint: string;
    queryKey: string;
    pageSize?: number;
}

export function useCrud<T extends { id: number }>({
    endpoint,
    queryKey,
    pageSize = 30,
}: UseCrudOptions) {
    const queryClient = useQueryClient();
    const [page, setPage] = useState(1);
    const [search, setSearch] = useState("");

    const listQuery = useQuery({
        queryKey: [queryKey, page, search],
        queryFn: () => {
            const url = search
                ? `${endpoint}?search=${encodeURIComponent(search)}&page=${page}&max_page=${pageSize}`
                : `${endpoint}?page=${page}&max_page=${pageSize}`;
            return api.get<PaginatedResponse<T>>(url);
        },
    });

    const createMutation = useMutation({
        mutationFn: (data: Partial<T>) => api.post<T>(endpoint, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [queryKey] });
            toast.success("Created successfully");
        },
        onError: (error: { detail?: string }) => {
            toast.error(error.detail || "Failed to create");
        },
    });

    const updateMutation = useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<T> }) =>
            api.put<T>(`${endpoint}${id}/`, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [queryKey] });
            toast.success("Updated successfully");
        },
        onError: (error: { detail?: string }) => {
            toast.error(error.detail || "Failed to update");
        },
    });

    const deleteMutation = useMutation({
        mutationFn: (id: number) => api.delete(`${endpoint}${id}/`),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [queryKey] });
            toast.success("Deleted successfully");
        },
        onError: (error: { detail?: string }) => {
            toast.error(error.detail || "Failed to delete");
        },
    });

    const totalPages = listQuery.data
        ? Math.ceil(listQuery.data.count / pageSize)
        : 0;

    const goToPage = useCallback(
        (p: number) => {
            if (p >= 1 && p <= totalPages) setPage(p);
        },
        [totalPages]
    );

    return {
        // Data
        data: listQuery.data?.results ?? [],
        totalCount: listQuery.data?.count ?? 0,
        totalPages,
        page,
        isLoading: listQuery.isLoading,
        isFetching: listQuery.isFetching,

        // Pagination
        goToPage,
        nextPage: () => goToPage(page + 1),
        prevPage: () => goToPage(page - 1),

        // Search
        search,
        setSearch,

        // Mutations
        create: createMutation.mutateAsync,
        update: (id: number, data: Partial<T>) =>
            updateMutation.mutateAsync({ id, data }),
        remove: deleteMutation.mutateAsync,
        isCreating: createMutation.isPending,
        isUpdating: updateMutation.isPending,
        isDeleting: deleteMutation.isPending,

        // Refetch
        refetch: listQuery.refetch,
    };
}
