from pathlib import Path
from typing import Any

import pandas as pd


class RecommendationService:
    def __init__(self) -> None:
        self.dataset = self._load_dataset()

        self.kerala_districts = {
            "thiruvananthapuram",
            "kollam",
            "pathanamthitta",
            "alappuzha",
            "kottayam",
            "idukki",
            "ernakulam",
            "thrissur",
            "palakkad",
            "malappuram",
            "kozhikode",
            "wayanad",
            "kannur",
            "kasaragod"
        }

        self.karnataka_districts = {
            "mysuru",
            "kodagu",
            "chikkamagaluru",
            "shivamogga",
            "udupi",
            "dakshina kannada",
            "hassan",
            "bengaluru",
            "belagavi",
            "ballari"
        }

    def _load_dataset(self) -> pd.DataFrame:
        project_root = Path.cwd().parent

        dataset_path = (
            project_root /
            "database" /
            "tourism.csv"
        )

        if not dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {dataset_path}"
            )

        dataframe = pd.read_csv(
            dataset_path
        )

        dataframe.columns = [
            column.strip()
            for column in dataframe.columns
        ]

        dataframe = dataframe.fillna("")

        return dataframe

    def get_all_destinations(
        self
    ) -> list[dict[str, Any]]:

        results = []

        for _, row in self.dataset.iterrows():
            results.append(
                {
                    "place_name": row.get(
                        "Name of the Place",
                        ""
                    ),
                    "district": row.get(
                        "District",
                        ""
                    ),
                    "description": row.get(
                        "Famous_For",
                        ""
                    ),
                    "activities": row.get(
                        "Activities",
                        ""
                    )
                }
            )

        return results

    def search_destination(
        self,
        query: str
    ) -> list[dict[str, Any]]:

        query = query.lower()

        results = []

        for _, row in self.dataset.iterrows():

            place_name = str(
                row.get(
                    "Name of the Place",
                    ""
                )
            ).lower()

            district = str(
                row.get(
                    "District",
                    ""
                )
            ).lower()

            description = str(
                row.get(
                    "Famous_For",
                    ""
                )
            ).lower()

            if (
                query in place_name
                or query in district
                or query in description
            ):
                results.append(
                    {
                        "place_name": row.get(
                            "Name of the Place",
                            ""
                        ),
                        "district": row.get(
                            "District",
                            ""
                        ),
                        "description": row.get(
                            "Famous_For",
                            ""
                        ),
                        "activities": row.get(
                            "Activities",
                            ""
                        )
                    }
                )

        return results

    def recommend_by_interest(
        self,
        interests: list[str]
    ) -> list[dict[str, Any]]:

        recommendations = []

        keywords = [
            interest.lower()
            for interest in interests
        ]

        for _, row in self.dataset.iterrows():

            description = str(
                row.get(
                    "Famous_For",
                    ""
                )
            ).lower()

            activities = str(
                row.get(
                    "Activities",
                    ""
                )
            ).lower()

            score = 0

            for keyword in keywords:

                if keyword in description:
                    score += 2

                if keyword in activities:
                    score += 3

            if score > 0:

                recommendations.append(
                    {
                        "place_name": row.get(
                            "Name of the Place",
                            ""
                        ),
                        "district": row.get(
                            "District",
                            ""
                        ),
                        "description": row.get(
                            "Famous_For",
                            ""
                        ),
                        "activities": row.get(
                            "Activities",
                            ""
                        ),
                        "match_score": score
                    }
                )

        recommendations.sort(
            key=lambda item:
            item["match_score"],
            reverse=True
        )

        return recommendations[:10]

    def recommend_eco_destinations(
        self
    ) -> list[dict[str, Any]]:

        eco_keywords = [
            "nature",
            "wildlife",
            "forest",
            "trekking",
            "hill",
            "waterfall",
            "lake",
            "eco",
            "green",
            "mountain"
        ]

        recommendations = []

        for _, row in self.dataset.iterrows():

            description = str(
                row.get(
                    "Famous_For",
                    ""
                )
            ).lower()

            activities = str(
                row.get(
                    "Activities",
                    ""
                )
            ).lower()

            score = 0

            for keyword in eco_keywords:

                if keyword in description:
                    score += 2

                if keyword in activities:
                    score += 3

            if score > 0:
                recommendations.append(
                    {
                        "place_name": row.get(
                            "Name of the Place",
                            ""
                        ),
                        "district": row.get(
                            "District",
                            ""
                        ),
                        "description": row.get(
                            "Famous_For",
                            ""
                        ),
                        "activities": row.get(
                            "Activities",
                            ""
                        ),
                        "eco_score": score
                    }
                )

        recommendations.sort(
            key=lambda item:
            item["eco_score"],
            reverse=True
        )

        return recommendations[:10]

    def get_kerala_destinations(
        self
    ) -> list[dict[str, Any]]:

        results = []

        for _, row in self.dataset.iterrows():

            district = str(
                row.get(
                    "District",
                    ""
                )
            ).lower()

            if district in self.kerala_districts:

                results.append(
                    {
                        "place_name": row.get(
                            "Name of the Place",
                            ""
                        ),
                        "district": row.get(
                            "District",
                            ""
                        ),
                        "description": row.get(
                            "Famous_For",
                            ""
                        ),
                        "activities": row.get(
                            "Activities",
                            ""
                        )
                    }
                )

        return results

    def get_karnataka_destinations(
        self
    ) -> list[dict[str, Any]]:

        results = []

        for _, row in self.dataset.iterrows():

            district = str(
                row.get(
                    "District",
                    ""
                )
            ).lower()

            if district in self.karnataka_districts:

                results.append(
                    {
                        "place_name": row.get(
                            "Name of the Place",
                            ""
                        ),
                        "district": row.get(
                            "District",
                            ""
                        ),
                        "description": row.get(
                            "Famous_For",
                            ""
                        ),
                        "activities": row.get(
                            "Activities",
                            ""
                        )
                    }
                )

        return results

    def recommend_by_budget(
        self,
        budget: float
    ) -> dict[str, Any]:

        if budget <= 10000:
            category = "Budget"

        elif budget <= 30000:
            category = "Standard"

        elif budget <= 60000:
            category = "Premium"

        else:
            category = "Luxury"

        return {
            "budget": budget,
            "recommended_category": category,
            "suggestions": [
                "Local transportation",
                "Regional cuisine",
                "Popular attractions",
                "Nature experiences"
            ]
        }

    def generate_destination_profile(
        self,
        destination_name: str
    ) -> dict[str, Any] | None:

        matches = self.search_destination(
            destination_name
        )

        if not matches:
            return None

        destination = matches[0]

        return {
            "destination": destination["place_name"],
            "district": destination["district"],
            "description": destination["description"],
            "activities": destination["activities"],
            "eco_friendly": True,
            "recommended_duration": "2-4 Days"
        }