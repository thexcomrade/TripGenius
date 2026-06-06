from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator


class WeatherSummarySchema(BaseModel):
    temperature: float | None = None
    condition: str | None = None
    humidity: int | None = None
    wind_speed: float | None = None
    visibility: int | None = None
    recommendation: str | None = None


class HotelRecommendationSchema(BaseModel):
    name: str
    category: str
    estimated_price: float
    rating: float | None = None
    location: str | None = None
    amenities: list[str] = Field(default_factory=list)


class RestaurantRecommendationSchema(BaseModel):
    name: str
    cuisine: str
    rating: float | None = None
    speciality: str | None = None


class AttractionSchema(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    estimated_duration_hours: float | None = None


class CostBreakdownSchema(BaseModel):
    accommodation_cost: float = 0.0
    transportation_cost: float = 0.0
    food_cost: float = 0.0
    miscellaneous_cost: float = 0.0
    total_cost: float = 0.0


class SustainabilitySchema(BaseModel):
    sustainability_score: int = 0
    carbon_footprint_estimate: float = 0.0
    eco_friendly_recommendations: list[str] = Field(
        default_factory=list
    )


class DayItinerarySchema(BaseModel):
    day: int

    title: str

    activities: list[str] = Field(
        default_factory=list
    )

    attractions: list[str] = Field(
        default_factory=list
    )

    meals: list[str] = Field(
        default_factory=list
    )

    accommodation: str | None = None

    transportation: str | None = None

    notes: str | None = None


class AITripGenerationRequest(BaseModel):
    destination: str = Field(
        min_length=2,
        max_length=200
    )

    duration_days: int = Field(
        ge=1,
        le=30
    )

    budget: float = Field(
        gt=0
    )

    travelers_count: int = Field(
        default=1,
        ge=1,
        le=20
    )

    travel_style: str | None = None

    interests: list[str] = Field(
        default_factory=list
    )

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    @field_validator("destination")
    @classmethod
    def validate_destination(
        cls,
        value: str
    ) -> str:

        cleaned_value = value.strip()

        if len(cleaned_value) < 2:
            raise ValueError(
                "Destination must contain at least 2 characters"
            )

        return cleaned_value


class TripCreateRequest(BaseModel):
    trip_title: str = Field(
        min_length=2,
        max_length=200
    )

    destination: str = Field(
        min_length=2,
        max_length=200
    )

    duration_days: int = Field(
        ge=1,
        le=30
    )

    budget: float = Field(
        gt=0
    )

    travelers_count: int = Field(
        default=1,
        ge=1,
        le=20
    )

    travel_style: str | None = None

    interests: list[str] = Field(
        default_factory=list
    )

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None


class TripUpdateRequest(BaseModel):
    trip_title: str | None = None

    destination: str | None = None

    duration_days: int | None = Field(
        default=None,
        ge=1,
        le=30
    )

    budget: float | None = Field(
        default=None,
        gt=0
    )

    travel_style: str | None = None

    transportation_mode: str | None = None

    preferred_accommodation: str | None = None

    interests: list[str] | None = None

    status: str | None = None

    is_favorite: bool | None = None

    is_public: bool | None = None


class TripResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    user_id: str

    trip_title: str

    destination: str

    state: str | None

    district: str | None

    duration_days: int

    travelers_count: int

    budget: float

    travel_style: str | None

    interests: list

    transportation_mode: str | None

    preferred_accommodation: str | None

    itinerary_summary: str | None

    estimated_trip_cost: float

    sustainability_score: int

    carbon_footprint_estimate: float

    ai_confidence_score: float

    status: str

    is_favorite: bool

    is_public: bool

    generated_by_ai: bool

    generation_model: str | None

    created_at: datetime

    updated_at: datetime


class CompleteTripResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    user_id: str

    trip_title: str

    destination: str

    state: str | None

    district: str | None

    duration_days: int

    travelers_count: int

    budget: float

    travel_style: str | None

    interests: list

    transportation_mode: str | None

    preferred_accommodation: str | None

    ai_itinerary: dict

    itinerary_summary: str | None

    attractions: list

    recommended_hotels: list

    recommended_restaurants: list

    local_cuisines: list

    beverages_to_try: list

    weather_summary: dict

    weather_alerts: list

    packing_checklist: list

    travel_tips: list

    accommodation_cost: float

    transportation_cost: float

    food_cost: float

    miscellaneous_cost: float

    estimated_trip_cost: float

    sustainability_score: int

    carbon_footprint_estimate: float

    eco_friendly_recommendations: list

    ai_confidence_score: float

    status: str

    is_favorite: bool

    is_public: bool

    generated_by_ai: bool

    generation_model: str | None

    created_at: datetime

    updated_at: datetime


class TripHistoryResponse(BaseModel):
    id: UUID

    trip_title: str

    destination: str

    duration_days: int

    budget: float

    sustainability_score: int

    status: str

    created_at: datetime


class TripStatisticsResponse(BaseModel):
    total_trips: int

    completed_trips: int

    favorite_trips: int

    total_budget_spent: float

    average_trip_budget: float

    average_sustainability_score: float


class DestinationRecommendationResponse(BaseModel):
    destination: str

    description: str

    activities: list[str]

    suitability_score: float


class MessageResponse(BaseModel):
    message: str


class AITripGenerationResponse(BaseModel):
    trip_title: str

    destination: str

    itinerary: list[DayItinerarySchema]

    attractions: list[AttractionSchema]

    hotels: list[HotelRecommendationSchema]

    restaurants: list[
        RestaurantRecommendationSchema
    ]

    weather: WeatherSummarySchema

    sustainability: SustainabilitySchema

    cost_breakdown: CostBreakdownSchema

    travel_tips: list[str]

    packing_checklist: list[str]