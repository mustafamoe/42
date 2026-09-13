from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        if not self.has_command_leader():
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365 and not self.has_experienced_long_crew():
            raise ValueError(
                "Long missions need 50% experienced crew (5+ years)"
            )
        if not self.has_only_active_crew():
            raise ValueError("All crew members must be active")
        return self

    def has_command_leader(self) -> bool:
        command_ranks = {Rank.COMMANDER, Rank.CAPTAIN}
        return any(member.rank in command_ranks for member in self.crew)

    def has_experienced_long_crew(self) -> bool:
        experienced_count = sum(
            member.years_experience >= 5 for member in self.crew
        )
        return experienced_count * 2 >= len(self.crew)

    def has_only_active_crew(self) -> bool:
        return all(member.is_active for member in self.crew)


def display_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )


def valid_crew() -> list[CrewMember]:
    return [
        CrewMember.model_validate(
            {
                "member_id": "CM001",
                "name": "Sarah Connor",
                "rank": "commander",
                "age": 45,
                "specialization": "Mission Command",
                "years_experience": 18,
            }
        ),
        CrewMember.model_validate(
            {
                "member_id": "CM002",
                "name": "John Smith",
                "rank": "lieutenant",
                "age": 36,
                "specialization": "Navigation",
                "years_experience": 8,
            }
        ),
        CrewMember.model_validate(
            {
                "member_id": "CM003",
                "name": "Alice Johnson",
                "rank": "officer",
                "age": 31,
                "specialization": "Engineering",
                "years_experience": 4,
            }
        ),
    ]


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    mission = SpaceMission.model_validate(
        {
            "mission_id": "M2024_MARS",
            "mission_name": "Mars Colony Establishment",
            "destination": "Mars",
            "launch_date": "2024-07-20T09:00:00",
            "duration_days": 900,
            "crew": valid_crew(),
            "budget_millions": 2500.0,
        }
    )
    display_mission(mission)

    print("=" * 41)
    print("Expected validation error:")

    try:
        SpaceMission.model_validate(
            {
                "mission_id": "M2024_LUNA",
                "mission_name": "Lunar Survey Mission",
                "destination": "Moon",
                "launch_date": "2024-05-12T08:00:00",
                "duration_days": 120,
                "crew": [
                    CrewMember.model_validate(
                        {
                            "member_id": "CM004",
                            "name": "Dana Lee",
                            "rank": "lieutenant",
                            "age": 34,
                            "specialization": "Science Officer",
                            "years_experience": 7,
                        }
                    )
                ],
                "budget_millions": 800.0,
            }
        )
    except ValidationError as error:
        first_error = error.errors()[0]
        print(first_error["msg"].removeprefix("Value error, "))


if __name__ == "__main__":
    main()
