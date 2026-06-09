import axios, {
    AxiosError,
    AxiosInstance
} from "axios";

const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_URL ??
    "http://127.0.0.1:8000";

export interface AITripRequest {
    destination: string;
    duration_days: number;
    budget: number;
    travelers_count: number;
    travel_style?: string;
    interests: string[];
    transportation_mode?: string;
    preferred_accommodation?: string;
}

export interface TripCreateRequest {
    trip_title: string;
    destination: string;
    duration_days: number;
    budget: number;
    travelers_count: number;
    travel_style?: string;
    interests: string[];
    transportation_mode?: string;
    preferred_accommodation?: string;
}

export interface TripResponse {
    id: string;
    user_id: string;
    trip_title: string;
    destination: string;
    duration_days: number;
    budget: number;
    status: string;
    created_at: string;
}

class TripService {
    private readonly api: AxiosInstance;

    constructor() {
        this.api = axios.create({
            baseURL: API_BASE_URL,
            timeout: 60000,
            headers: {
                "Content-Type":
                    "application/json"
            }
        });

        this.api.interceptors.request.use(
            (config) => {
                const token =
                    localStorage.getItem(
                        "tripgenius_token"
                    );

                if (
                    token &&
                    config.headers
                ) {
                    config.headers.Authorization =
                        `Bearer ${token}`;
                }

                return config;
            }
        );
    }

    async generateAIItinerary(
        payload: AITripRequest
    ): Promise<any> {
        try {
            const response =
                await this.api.post(
                    "/api/trips/generate-ai-itinerary",
                    payload
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async createTrip(
        payload: TripCreateRequest
    ): Promise<TripResponse> {
        try {
            const response =
                await this.api.post<TripResponse>(
                    "/api/trips/create",
                    payload
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async getTrip(
        tripId: string
    ): Promise<any> {
        try {
            const response =
                await this.api.get(
                    `/api/trips/${tripId}`
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async updateTrip(
        tripId: string,
        payload: any
    ): Promise<any> {
        try {
            const response =
                await this.api.put(
                    `/api/trips/${tripId}`,
                    payload
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async deleteTrip(
        tripId: string
    ): Promise<void> {
        try {
            await this.api.delete(
                `/api/trips/${tripId}`
            );
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async getHistory(): Promise<any> {
        try {
            const response =
                await this.api.get(
                    "/api/trips/history"
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async getStatistics(): Promise<any> {
        try {
            const response =
                await this.api.get(
                    "/api/trips/statistics"
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async favoriteTrip(
        tripId: string
    ): Promise<any> {
        try {
            const response =
                await this.api.post(
                    `/api/trips/${tripId}/favorite`
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    async unfavoriteTrip(
        tripId: string
    ): Promise<any> {
        try {
            const response =
                await this.api.post(
                    `/api/trips/${tripId}/unfavorite`
                );

            return response.data;
        } catch (error) {
            throw this.handleError(
                error
            );
        }
    }

    private handleError(
        error: unknown
    ): Error {
        if (
            axios.isAxiosError(error)
        ) {
            const axiosError =
                error as AxiosError<any>;

            const message =
                axiosError.response
                    ?.data?.detail ||
                axiosError.response
                    ?.data?.message ||
                axiosError.message ||
                "Request failed";

            return new Error(
                message
            );
        }

        return new Error(
            "Unexpected error occurred"
        );
    }
}

export const tripService =
    new TripService();

export default tripService;
