from __future__ import annotations

import json
import logging
import time
from functools import lru_cache
from typing import Any

from google import genai

from app.core.config import settings

from app.services.weather_service import (
    WeatherService
)

from app.services.recommendation_service import (
    RecommendationService
)


logger = logging.getLogger(__name__)


class AIService:
    """
    ==================================================
    TripGenius AI Engine
    ==================================================

    Responsibilities

    ✓ Gemini Initialization
    ✓ Prompt Templates
    ✓ Destination Summary Generator
    ✓ Weather Integration
    ✓ Recommendation Integration
    ✓ Attraction Generator
    ✓ Activity Generator
    ✓ Hotel Generator
    ✓ Restaurant Generator
    ✓ Cuisine Generator
    ✓ Beverage Generator
    ✓ Packing Generator
    ✓ Travel Tips Generator
    ✓ Cost Estimator
    ✓ Sustainability Scoring
    ✓ Carbon Footprint Estimator
    ✓ Eco Recommendation Generator
    ✓ AI Confidence Scoring
    ✓ Day Wise Itinerary Generator
    ✓ Response Validation
    ✓ Retry Logic
    ✓ Offline Fallback
    ✓ Cache Layer
    ✓ JSON Formatter
    """

    MAX_RETRIES = 3

    def __init__(self) -> None:

        self.weather_service = (
            WeatherService()
        )

        self.recommendation_service = (
            RecommendationService()
        )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = (
            "gemini-2.5-flash"
        )

    # ==================================================
    # Prompt Templates
    # ==================================================

    def _build_master_prompt(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str],
        travel_style: str | None = None
    ) -> str:

        return f"""
You are TripGenius AI.

Generate a professional travel plan.

Destination:
{destination}

Duration:
{duration_days} Days

Budget:
₹{budget}

Interests:
{", ".join(interests)}

Travel Style:
{travel_style or "General"}

Generate:

1. Trip Title

2. Destination Summary

3. Day Wise Itinerary

4. Recommended Attractions

5. Recommended Activities

6. Recommended Hotels

7. Recommended Restaurants

8. Local Cuisine Suggestions

9. Beverages To Try

10. Packing Checklist

11. Travel Tips

12. Eco Friendly Suggestions

Return JSON only.
"""

    def _build_itinerary_prompt(
        self,
        destination: str,
        duration_days: int,
        interests: list[str]
    ) -> str:

        return f"""
Create a detailed day-wise itinerary.

Destination:
{destination}

Duration:
{duration_days}

Interests:
{", ".join(interests)}

Return JSON.
"""

    def _build_hotel_prompt(
        self,
        destination: str,
        budget: float
    ) -> str:

        return f"""
Recommend hotels for:

Destination:
{destination}

Budget:
₹{budget}

Return list only.
"""

    def _build_food_prompt(
        self,
        destination: str
    ) -> str:

        return f"""
Recommend local cuisines,
restaurants and beverages.

Destination:
{destination}

Return JSON.
"""

    # ==================================================
    # Gemini Communication Layer
    # ==================================================

    def _generate_content(
        self,
        prompt: str
    ) -> str:

        last_error = None

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model=self.model_name,
                        contents=prompt
                    )
                )

                if (
                    response
                    and response.text
                ):
                    return response.text

            except Exception as error:

                last_error = error

                logger.warning(
                    (
                        "Gemini attempt %s failed: %s"
                    ),
                    attempt + 1,
                    str(error)
                )

                time.sleep(2)

        raise RuntimeError(
            f"Gemini generation failed: "
            f"{last_error}"
        )

    # ==================================================
    # JSON Parsing Utilities
    # ==================================================

    def _safe_json_parse(
        self,
        content: str
    ) -> dict[str, Any]:

        try:

            cleaned = (
                content
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

            parsed = json.loads(
                cleaned
            )

            if isinstance(
                parsed,
                dict
            ):
                return parsed

        except Exception:
            pass

        return {}

    # ==================================================
    # Cache Layer
    # ==================================================

    @lru_cache(maxsize=100)
    def _cached_destination_profile(
        self,
        destination: str
    ) -> dict[str, Any] | None:

        return (
            self.recommendation_service
            .generate_destination_profile(
                destination
            )
        )

    # ==================================================
    # Weather Integration
    # ==================================================

    def get_weather_context(
        self,
        destination: str
    ) -> dict[str, Any]:

        try:

            return (
                self.weather_service
                .get_current_weather(
                    destination
                )
            )

        except Exception as error:

            logger.warning(
                "Weather fetch failed: %s",
                str(error)
            )

            return {
                "city": destination,
                "temperature": 0,
                "condition": "Unknown",
                "humidity": 0,
                "travel_recommendation":
                    "Weather data unavailable.",
                "packing_suggestions": []
            }

    # ==================================================
    # Recommendation Integration
    # ==================================================

    def get_recommendation_context(
        self,
        destination: str,
        interests: list[str],
        budget: float
    ) -> dict[str, Any]:

        recommendations = (
            self.recommendation_service
            .recommend_by_interest(
                interests
            )
        )

        budget_plan = (
            self.recommendation_service
            .recommend_by_budget(
                budget
            )
        )

        destination_profile = (
            self._cached_destination_profile(
                destination
            )
        )

        return {
            "destination_profile":
                destination_profile,

            "recommendations":
                recommendations,

            "budget_plan":
                budget_plan
        }

    # ==================================================
    # Destination Summary Generator
    # ==================================================

    def generate_destination_summary(
        self,
        destination: str
    ) -> str:

        profile = (
            self._cached_destination_profile(
                destination
            )
        )

        if profile:

            return (
                profile.get(
                    "description",
                    ""
                )
            )

        return (
            f"{destination} is a wonderful "
            f"travel destination offering "
            f"culture, attractions and "
            f"memorable experiences."
        )
    # ==================================================
    # Attraction Generator
    # ==================================================

    def generate_attractions(
        self,
        destination: str,
        interests: list[str]
    ) -> list[str]:

        recommendations = (
            self.recommendation_service
            .recommend_by_interest(
                interests
            )
        )

        attractions: list[str] = []

        for item in recommendations[:10]:

            place_name = item.get(
                "place_name",
                ""
            )

            if (
                place_name
                and place_name not in attractions
            ):
                attractions.append(
                    place_name
                )

        if attractions:
            return attractions

        return [
            f"{destination} Town Center",
            f"{destination} View Point",
            f"{destination} Cultural Area"
        ]

    # ==================================================
    # Activity Generator
    # ==================================================

    def generate_activities(
        self,
        interests: list[str]
    ) -> list[str]:

        activity_map = {
            "nature": [
                "Nature Walk",
                "Forest Exploration",
                "Wildlife Observation"
            ],
            "trekking": [
                "Mountain Trekking",
                "Hill Hiking",
                "Adventure Trails"
            ],
            "photography": [
                "Sunrise Photography",
                "Landscape Photography",
                "Street Photography"
            ],
            "food": [
                "Food Tour",
                "Local Cuisine Experience"
            ],
            "culture": [
                "Temple Visits",
                "Museum Tours",
                "Cultural Shows"
            ],
            "adventure": [
                "Zipline",
                "Camping",
                "Rock Climbing"
            ]
        }

        activities: list[str] = []

        for interest in interests:

            matched = activity_map.get(
                interest.lower(),
                []
            )

            activities.extend(
                matched
            )

        if not activities:

            activities = [
                "Sightseeing",
                "Local Exploration",
                "Photography"
            ]

        return list(
            dict.fromkeys(
                activities
            )
        )

    # ==================================================
    # Hotel Generator
    # ==================================================

    def generate_hotels(
        self,
        destination: str,
        budget: float
    ) -> list[str]:

        if budget <= 10000:

            return [
                f"{destination} Budget Inn",
                f"{destination} Backpackers Hostel",
                f"{destination} Guest House"
            ]

        if budget <= 30000:

            return [
                f"{destination} Eco Residency",
                f"{destination} Nature Resort",
                f"{destination} Comfort Stay"
            ]

        if budget <= 60000:

            return [
                f"{destination} Premium Resort",
                f"{destination} Hill View Resort",
                f"{destination} Boutique Hotel"
            ]

        return [
            f"{destination} Luxury Resort",
            f"{destination} Grand Palace Hotel",
            f"{destination} Five Star Retreat"
        ]

    # ==================================================
    # Restaurant Generator
    # ==================================================

    def generate_restaurants(
        self,
        destination: str
    ) -> list[str]:

        return [
            f"{destination} Spice Garden",
            f"{destination} Traditional Kitchen",
            f"{destination} Family Restaurant",
            f"{destination} Food Court",
            f"{destination} Heritage Dining"
        ]

    # ==================================================
    # Cuisine Generator
    # ==================================================

    def generate_local_cuisines(
        self,
        destination: str
    ) -> list[str]:

        destination_lower = (
            destination.lower()
        )

        if (
            "munnar" in destination_lower
            or "kerala" in destination_lower
        ):

            return [
                "Appam",
                "Puttu",
                "Kerala Sadya",
                "Malabar Biryani",
                "Karimeen Pollichathu"
            ]

        if (
            "coorg" in destination_lower
            or "kodagu" in destination_lower
        ):

            return [
                "Pandi Curry",
                "Kadambuttu",
                "Akki Roti",
                "Bamboo Shoot Curry"
            ]

        return [
            "Regional Cuisine",
            "Traditional Meals",
            "Street Food",
            "Local Specialities"
        ]

    # ==================================================
    # Beverage Generator
    # ==================================================

    def generate_beverages(
        self,
        destination: str
    ) -> list[str]:

        destination_lower = (
            destination.lower()
        )

        if (
            "munnar" in destination_lower
        ):

            return [
                "Fresh Tea",
                "Cardamom Tea",
                "Lemon Tea",
                "Herbal Tea"
            ]

        return [
            "Fresh Juice",
            "Local Tea",
            "Traditional Drinks"
        ]

    # ==================================================
    # Packing Checklist Generator
    # ==================================================

    def generate_packing_checklist(
        self,
        destination: str
    ) -> list[str]:

        weather = (
            self.get_weather_context(
                destination
            )
        )

        checklist = [
            "Government ID",
            "Mobile Charger",
            "Power Bank",
            "Water Bottle",
            "Personal Medicines",
            "Cash",
            "Travel Documents"
        ]

        checklist.extend(
            weather.get(
                "packing_suggestions",
                []
            )
        )

        return list(
            dict.fromkeys(
                checklist
            )
        )

    # ==================================================
    # Travel Tips Generator
    # ==================================================

    def generate_travel_tips(
        self,
        destination: str
    ) -> list[str]:

        return [
            "Book accommodations early.",
            "Carry valid identification.",
            "Respect local culture.",
            "Keep emergency contacts handy.",
            "Use reusable water bottles.",
            "Avoid littering.",
            "Check weather forecasts daily.",
            "Keep digital copies of documents."
        ]

    # ==================================================
    # Cost Estimator
    # ==================================================

    def estimate_trip_cost(
        self,
        budget: float,
        duration_days: int,
        travelers_count: int
    ) -> dict[str, float]:

        total_budget = (
            budget * travelers_count
        )

        accommodation_cost = round(
            total_budget * 0.40,
            2
        )

        food_cost = round(
            total_budget * 0.20,
            2
        )

        transportation_cost = round(
            total_budget * 0.25,
            2
        )

        miscellaneous_cost = round(
            total_budget * 0.15,
            2
        )

        estimated_trip_cost = (
            accommodation_cost
            + food_cost
            + transportation_cost
            + miscellaneous_cost
        )

        return {
            "estimated_trip_cost":
                estimated_trip_cost,

            "accommodation_cost":
                accommodation_cost,

            "food_cost":
                food_cost,

            "transportation_cost":
                transportation_cost,

            "miscellaneous_cost":
                miscellaneous_cost
        }
    # ==================================================
    # Sustainability Score Engine
    # ==================================================

    def calculate_sustainability_score(
        self,
        interests: list[str],
        transportation_mode: str | None = None
    ) -> int:

        score = 50

        eco_interests = {
            "nature",
            "eco",
            "wildlife",
            "trekking",
            "photography"
        }

        for interest in interests:

            if (
                interest.lower()
                in eco_interests
            ):
                score += 5

        if transportation_mode:

            transport = (
                transportation_mode.lower()
            )

            if transport in [
                "walking",
                "cycling"
            ]:
                score += 20

            elif transport in [
                "train",
                "bus"
            ]:
                score += 10

            elif transport in [
                "car"
            ]:
                score += 5

            elif transport in [
                "flight",
                "air"
            ]:
                score -= 10

        return max(
            0,
            min(
                score,
                100
            )
        )

    # ==================================================
    # Carbon Footprint Estimator
    # ==================================================

    def estimate_carbon_footprint(
        self,
        duration_days: int,
        transportation_mode: str | None
    ) -> float:

        transport_factor = {
            "walking": 1.0,
            "cycling": 1.5,
            "bus": 3.0,
            "train": 4.0,
            "car": 8.0,
            "flight": 25.0,
            "air": 25.0
        }

        factor = transport_factor.get(
            (
                transportation_mode or "car"
            ).lower(),
            8.0
        )

        footprint = (
            factor *
            duration_days
        )

        return round(
            footprint,
            2
        )

    # ==================================================
    # Eco Friendly Recommendation Generator
    # ==================================================

    def generate_eco_recommendations(
        self
    ) -> list[str]:

        return [
            "Carry a reusable water bottle.",
            "Avoid single-use plastics.",
            "Use public transportation whenever possible.",
            "Support local businesses and guides.",
            "Follow Leave No Trace principles.",
            "Respect wildlife and natural habitats.",
            "Use eco-friendly accommodations.",
            "Reduce food waste during travel."
        ]

    # ==================================================
    # AI Confidence Calculator
    # ==================================================

    def calculate_ai_confidence(
        self,
        weather_available: bool,
        recommendations_count: int,
        destination_profile_found: bool
    ) -> float:

        confidence = 60.0

        if weather_available:
            confidence += 15.0

        if (
            recommendations_count >= 5
        ):
            confidence += 15.0

        elif (
            recommendations_count >= 2
        ):
            confidence += 10.0

        if destination_profile_found:
            confidence += 10.0

        return round(
            min(
                confidence,
                100.0
            ),
            2
        )

    # ==================================================
    # Day Wise Itinerary Generator
    # ==================================================

    def generate_day_wise_itinerary(
        self,
        destination: str,
        duration_days: int,
        interests: list[str]
    ) -> list[dict[str, Any]]:

        activities = (
            self.generate_activities(
                interests
            )
        )

        itinerary = []

        activity_index = 0

        for day in range(
            1,
            duration_days + 1
        ):

            day_plan = {
                "day": day,
                "title":
                    f"Day {day}",
                "destination":
                    destination,
                "morning": "",
                "afternoon": "",
                "evening": ""
            }

            if day == 1:

                day_plan["title"] = (
                    "Arrival & Exploration"
                )

                day_plan["morning"] = (
                    "Arrival and hotel check-in"
                )

                day_plan["afternoon"] = (
                    "Local sightseeing"
                )

                day_plan["evening"] = (
                    "Relax and explore local markets"
                )

            elif day == duration_days:

                day_plan["title"] = (
                    "Departure Day"
                )

                day_plan["morning"] = (
                    "Breakfast and souvenir shopping"
                )

                day_plan["afternoon"] = (
                    "Visit nearby attraction"
                )

                day_plan["evening"] = (
                    "Departure"
                )

            else:

                morning_activity = (
                    activities[
                        activity_index
                        % len(
                            activities
                        )
                    ]
                )

                afternoon_activity = (
                    activities[
                        (
                            activity_index + 1
                        )
                        % len(
                            activities
                        )
                    ]
                )

                evening_activity = (
                    activities[
                        (
                            activity_index + 2
                        )
                        % len(
                            activities
                        )
                    ]
                )

                day_plan["morning"] = (
                    morning_activity
                )

                day_plan["afternoon"] = (
                    afternoon_activity
                )

                day_plan["evening"] = (
                    evening_activity
                )

                activity_index += 3

            itinerary.append(
                day_plan
            )

        return itinerary

    # ==================================================
    # Gemini Response Parser
    # ==================================================

    def parse_gemini_response(
        self,
        response_text: str
    ) -> dict[str, Any]:

        parsed = (
            self._safe_json_parse(
                response_text
            )
        )

        if parsed:
            return parsed

        return {
            "raw_response":
                response_text
        }

    # ==================================================
    # Offline Fallback Generator
    # ==================================================

    def generate_offline_trip_plan(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str]
    ) -> dict[str, Any]:

        attractions = (
            self.generate_attractions(
                destination,
                interests
            )
        )

        activities = (
            self.generate_activities(
                interests
            )
        )

        return {
            "trip_title":
                f"{destination} Adventure",

            "destination_summary":
                self.generate_destination_summary(
                    destination
                ),

            "attractions":
                attractions,

            "activities":
                activities,

            "itinerary":
                self.generate_day_wise_itinerary(
                    destination,
                    duration_days,
                    interests
                )
        }

    # ==================================================
    # Validation Methods
    # ==================================================

    def validate_trip_input(
        self,
        destination: str,
        duration_days: int,
        budget: float
    ) -> None:

        if not destination:
            raise ValueError(
                "Destination is required."
            )

        if duration_days <= 0:
            raise ValueError(
                "Duration must be greater than zero."
            )

        if budget <= 0:
            raise ValueError(
                "Budget must be greater than zero."
            )

    # ==================================================
    # Retry Logic
    # ==================================================

    def execute_with_retry(
        self,
        function,
        *args,
        **kwargs
    ):

        last_error = None

        for _ in range(
            self.MAX_RETRIES
        ):

            try:

                return function(
                    *args,
                    **kwargs
                )

            except Exception as error:

                last_error = error

                time.sleep(1)

        raise RuntimeError(
            f"Operation failed: "
            f"{last_error}"
        )
    # ==================================================
    # JSON Formatter
    # ==================================================

    def format_trip_response(
        self,
        data: dict[str, Any]
    ) -> dict[str, Any]:

        return {
            key: value
            for key, value in data.items()
            if value is not None
        }

    # ==================================================
    # Final AI Response Builder
    # ==================================================

    def build_complete_response(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        travelers_count: int,
        interests: list[str],
        transportation_mode: str | None = None
    ) -> dict[str, Any]:

        weather = (
            self.get_weather_context(
                destination
            )
        )

        recommendation_context = (
            self.get_recommendation_context(
                destination,
                interests,
                budget
            )
        )

        attractions = (
            self.generate_attractions(
                destination,
                interests
            )
        )

        activities = (
            self.generate_activities(
                interests
            )
        )

        hotels = (
            self.generate_hotels(
                destination,
                budget
            )
        )

        restaurants = (
            self.generate_restaurants(
                destination
            )
        )

        cuisines = (
            self.generate_local_cuisines(
                destination
            )
        )

        beverages = (
            self.generate_beverages(
                destination
            )
        )

        packing = (
            self.generate_packing_checklist(
                destination
            )
        )

        tips = (
            self.generate_travel_tips(
                destination
            )
        )

        cost_data = (
            self.estimate_trip_cost(
                budget,
                duration_days,
                travelers_count
            )
        )

        sustainability_score = (
            self.calculate_sustainability_score(
                interests,
                transportation_mode
            )
        )

        carbon_footprint = (
            self.estimate_carbon_footprint(
                duration_days,
                transportation_mode
            )
        )

        eco_recommendations = (
            self.generate_eco_recommendations()
        )

        itinerary = (
            self.generate_day_wise_itinerary(
                destination,
                duration_days,
                interests
            )
        )

        destination_profile = (
            recommendation_context.get(
                "destination_profile"
            )
        )

        confidence = (
            self.calculate_ai_confidence(
                weather_available=True,
                recommendations_count=len(
                    recommendation_context.get(
                        "recommendations",
                        []
                    )
                ),
                destination_profile_found=
                destination_profile is not None
            )
        )

        return {
            "trip_title":
                f"{destination} Travel Experience",

            "destination_summary":
                self.generate_destination_summary(
                    destination
                ),

            "weather_summary":
                weather,

            "attractions":
                attractions,

            "activities":
                activities,

            "recommended_hotels":
                hotels,

            "recommended_restaurants":
                restaurants,

            "local_cuisines":
                cuisines,

            "beverages_to_try":
                beverages,

            "packing_checklist":
                packing,

            "travel_tips":
                tips,

            "ai_itinerary":
                itinerary,

            "sustainability_score":
                sustainability_score,

            "carbon_footprint_estimate":
                carbon_footprint,

            "eco_friendly_recommendations":
                eco_recommendations,

            "ai_confidence_score":
                confidence,

            **cost_data
        }

    # ==================================================
    # Master Trip Plan Generator
    # ==================================================

    def generate_trip_plan(
        self,
        destination: str,
        duration_days: int,
        budget: float,
        interests: list[str],
        travelers_count: int = 1,
        travel_style: str | None = None,
        transportation_mode: str | None = None
    ) -> dict[str, Any]:

        self.validate_trip_input(
            destination,
            duration_days,
            budget
        )

        try:

            prompt = (
                self._build_master_prompt(
                    destination=destination,
                    duration_days=duration_days,
                    budget=budget,
                    interests=interests,
                    travel_style=travel_style
                )
            )

            ai_response = (
                self.execute_with_retry(
                    self._generate_content,
                    prompt
                )
            )

            parsed_ai_response = (
                self.parse_gemini_response(
                    ai_response
                )
            )

            base_response = (
                self.build_complete_response(
                    destination=destination,
                    duration_days=duration_days,
                    budget=budget,
                    travelers_count=travelers_count,
                    interests=interests,
                    transportation_mode=
                    transportation_mode
                )
            )

            if parsed_ai_response:

                base_response[
                    "gemini_response"
                ] = parsed_ai_response

            return (
                self.format_trip_response(
                    base_response
                )
            )

        except Exception as error:

            logger.exception(
                "AI Trip Generation Failed: %s",
                str(error)
            )

            fallback = (
                self.generate_offline_trip_plan(
                    destination=destination,
                    duration_days=duration_days,
                    budget=budget,
                    interests=interests
                )
            )

            fallback[
                "error"
            ] = str(error)

            fallback[
                "generation_mode"
            ] = "offline"

            return fallback


# ==================================================
# Singleton Instance
# ==================================================

_ai_service_instance = None


def get_ai_service() -> AIService:

    global _ai_service_instance

    if _ai_service_instance is None:

        _ai_service_instance = (
            AIService()
        )

    return _ai_service_instance