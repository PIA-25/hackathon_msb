"""
Game Data Service
-----------------
A clean interface for the game engine to fetch and interact with game data.
This module provides easy-to-use functions that return data in formats
optimized for the NiceGUI game frontend.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

# Import your existing modules
from . import models
from .crud import (
    get_scenario,
    get_choice_options,
    get_level,
    get_user,
    save_user_choice_and_update_attributes,
    get_user_attributes,
    create_user
)
from .database import SessionLocal

logger = logging.getLogger(__name__)


# -------------------------------------------------------
# DATA CLASSES FOR GAME ENGINE
# -------------------------------------------------------
@dataclass
class GameChoice:
    """Represents a single choice option for the game UI"""
    choice_id: int
    text: str  # option_text - what player sees
    outcome_text: str  # feedback after choosing
    is_correct: bool  # True = good choice, False = bad choice, None = neutral

    def to_dict(self) -> Dict:
        return {
            'choice_id': self.choice_id,
            'text': self.text,
            'outcome_text': self.outcome_text,
            'is_correct': self.is_correct
        }


@dataclass
class GameScenario:
    """Represents a scenario with all its choices for the game UI"""
    scenario_id: int
    level_id: int
    level_number: int
    level_title: str
    scenario_text: str
    choices: List[GameChoice] = field(default_factory=list)

    # Optional: paths to media files (you can extend the DB schema later)
    video_path: Optional[str] = None
    image_correct: Optional[str] = None
    image_wrong: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            'scenario_id': self.scenario_id,
            'level_id': self.level_id,
            'level_number': self.level_number,
            'level_title': self.level_title,
            'text': self.scenario_text,
            'choices': [c.to_dict() for c in self.choices],
            'video_path': self.video_path,
            'image_correct': self.image_correct,
            'image_wrong': self.image_wrong
        }

    def get_correct_choice(self) -> Optional[GameChoice]:
        """Returns the first correct choice (is_good=True)"""
        for choice in self.choices:
            if choice.is_correct is True:
                return choice
        return None

    def get_wrong_choices(self) -> List[GameChoice]:
        """Returns all wrong choices (is_good=False)"""
        return [c for c in self.choices if c.is_correct is False]


@dataclass
class GameLevel:
    """Represents a level with all its scenarios"""
    level_id: int
    level_number: int
    title: str
    scenarios: List[GameScenario] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'level_id': self.level_id,
            'level_number': self.level_number,
            'title': self.title,
            'scenarios': [s.to_dict() for s in self.scenarios]
        }


# -------------------------------------------------------
# DATABASE SESSION HELPER
# -------------------------------------------------------
def get_db() -> Session:
    """Get a new database session"""
    return SessionLocal()


# -------------------------------------------------------
# GAME DATA FETCHING FUNCTIONS
# -------------------------------------------------------
def fetch_scenario_for_game(scenario_id: int) -> Optional[GameScenario]:
    """
    Fetch a single scenario with all its choices, formatted for the game engine.

    Args:
        scenario_id: The scenario ID to fetch

    Returns:
        GameScenario object or None if not found
    """
    db = get_db()
    try:
        scenario = get_scenario(db, scenario_id)
        if not scenario:
            return None

        level = get_level(db, scenario.level_id)
        choices = get_choice_options(db, scenario_id)

        game_choices = [
            GameChoice(
                choice_id=c.choice_id,
                text=c.option_text,
                outcome_text=c.outcome_text,
                is_correct=c.is_good
            )
            for c in choices
        ]

        return GameScenario(
            scenario_id=scenario.scenario_id,
            level_id=scenario.level_id,
            level_number=level.level_number if level else 0,
            level_title=level.title if level else "",
            scenario_text=scenario.scenario_text,
            choices=game_choices,
            # You can add video/image paths here if you extend the schema
            video_path=f"videos/scenario_{scenario_id}.mp4",
            image_correct=f"images/scenario_{scenario_id}_correct.png",
            image_wrong=f"images/scenario_{scenario_id}_wrong.png"
        )
    except SQLAlchemyError as e:
        logger.error(f"Error fetching scenario {scenario_id}: {e}")
        return None
    finally:
        db.close()


def fetch_level_scenarios(level_id: int) -> List[GameScenario]:
    """
    Fetch all scenarios for a specific level.

    Args:
        level_id: The level ID to fetch scenarios for

    Returns:
        List of GameScenario objects
    """
    db = get_db()
    try:
        level = get_level(db, level_id)
        if not level:
            return []

        scenarios = db.query(models.Scenario).filter(
            models.Scenario.level_id == level_id
        ).order_by(models.Scenario.scenario_id).all()

        game_scenarios = []
        for scenario in scenarios:
            choices = get_choice_options(db, scenario.scenario_id)
            game_choices = [
                GameChoice(
                    choice_id=c.choice_id,
                    text=c.option_text,
                    outcome_text=c.outcome_text,
                    is_correct=c.is_good
                )
                for c in choices
            ]

            game_scenarios.append(GameScenario(
                scenario_id=scenario.scenario_id,
                level_id=level_id,
                level_number=level.level_number,
                level_title=level.title or "",
                scenario_text=scenario.scenario_text,
                choices=game_choices,
                video_path=f"videos/scenario_{scenario.scenario_id}.mp4",
                image_correct=f"images/scenario_{scenario.scenario_id}_correct.png",
                image_wrong=f"images/scenario_{scenario.scenario_id}_wrong.png"
            ))

        return game_scenarios
    except SQLAlchemyError as e:
        logger.error(f"Error fetching level scenarios for level {level_id}: {e}")
        return []
    finally:
        db.close()


def fetch_all_levels() -> List[GameLevel]:
    """
    Fetch all levels with their scenarios, ready for the game engine.

    Returns:
        List of GameLevel objects with nested scenarios
    """
    db = get_db()
    try:
        levels = db.query(models.Level).order_by(models.Level.level_number).all()

        game_levels = []
        for level in levels:
            scenarios = fetch_level_scenarios(level.level_id)
            game_levels.append(GameLevel(
                level_id=level.level_id,
                level_number=level.level_number,
                title=level.title or "",
                scenarios=scenarios
            ))

        return game_levels
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all levels: {e}")
        return []
    finally:
        db.close()


def fetch_all_scenarios_flat() -> List[Dict]:
    """
    Fetch all scenarios as a flat list of dictionaries.
    This is the simplest format for the game engine, similar to your mock. json structure.

    Returns:
        List of scenario dictionaries ready for GameUI class
    """
    db = get_db()
    try:
        # Get all scenarios ordered by level and scenario ID
        scenarios = db.query(models.Scenario).join(models.Level).order_by(
            models.Level.level_number,
            models.Scenario.scenario_id
        ).all()

        result = []
        for scenario in scenarios:
            choices = get_choice_options(db, scenario.scenario_id)
            level = get_level(db, scenario.level_id)

            # Find correct and wrong choices
            correct_choice = next((c for c in choices if c.is_good is True), None)
            wrong_choice = next((c for c in choices if c.is_good is False), None)

            # Format similar to your original mock.json structure
            scenario_dict = {
                'id': scenario.scenario_id,
                'level_id': scenario.level_id,
                'level_number': level.level_number if level else 0,
                'level_title': level.title if level else "",
                'text': scenario.scenario_text,

                # Choice texts (A and B)
                'a': choices[0].option_text if len(choices) > 0 else "",
                'b': choices[1].option_text if len(choices) > 1 else "",

                # Which one is correct ('a' or 'b')
                'correct': 'a' if (len(choices) > 0 and choices[0].is_good) else 'b',

                # Feedback messages
                'wrong_msg': wrong_choice.outcome_text if wrong_choice else "",
                'right_msg': correct_choice.outcome_text if correct_choice else "",

                # All choices with IDs (for saving to database)
                'choices': [
                    {
                        'choice_id': c.choice_id,
                        'text': c.option_text,
                        'outcome_text': c.outcome_text,
                        'is_good': c.is_good,
                        'label': chr(97 + i)  # 'a', 'b', 'c', etc.
                    }
                    for i, c in enumerate(choices)
                ],

                # Media paths
                'video_path': f"videos/scenario_{scenario.scenario_id}.mp4",
                'video_correct': f"videos/scenario_{scenario.scenario_id}_correct.mp4",
                'video_wrong': f"videos/scenario_{scenario.scenario_id}_wrong. mp4",
            }
            result.append(scenario_dict)

        return result
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all scenarios: {e}")
        return []
    finally:
        db.close()


# -------------------------------------------------------
# GAME STATE / USER INTERACTION FUNCTIONS
# -------------------------------------------------------
def register_player(firstname: str, lastname: str, age: int, krigsberedd: Optional[bool] = None) -> Optional[int]:
    """
    Register a new player and return their user_id.

    Returns:
        user_id if successful, None if failed
    """
    db = get_db()
    try:
        user = create_user(db, firstname, lastname, age, krigsberedd)
        return user.user_id if user else None
    except SQLAlchemyError as e:
        logger.error(f"Error registering player: {e}")
        return None
    finally:
        db.close()


def record_player_choice(user_id: int, level_id: int, scenario_id: int, choice_id: int) -> bool:
    """
    Record a player's choice and update their attributes.

    Args:
        user_id: Player's user ID
        level_id: Current level ID
        scenario_id: Current scenario ID
        choice_id: The choice the player made

    Returns:
        True if successful, False if failed
    """
    db = get_db()
    try:
        result = save_user_choice_and_update_attributes(
            db, user_id, level_id, scenario_id, choice_id
        )
        return result is not None
    except SQLAlchemyError as e:
        logger.error(f"Error recording player choice: {e}")
        return False
    finally:
        db.close()


def get_player_profile(user_id: int) -> Optional[Dict]:
    """
    Get a player's profile including their attributes and scores.

    Returns:
        Dictionary with player info and attributes, or None if not found
    """
    db = get_db()
    try:
        user = get_user(db, user_id)
        if not user:
            return None

        attributes = get_user_attributes(db, user_id)

        return {
            'user_id': user.user_id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'age': user.age,
            'krigsberedd': user.krigsberedd,
            'created_at': str(user.created_at),
            'attributes': attributes
        }
    except SQLAlchemyError as e:
        logger.error(f"Error getting player profile: {e}")
        return None
    finally:
        db.close()


# -------------------------------------------------------
# CONVENIENCE CLASS FOR GAME ENGINE
# -------------------------------------------------------
class GameDataProvider:
    """
    A convenience class that provides all game data through a single interface.
    Use this in your main. py instead of calling individual functions.
    """

    def __init__(self):
        self._scenarios: List[Dict] = []
        self._current_user_id: Optional[int] = None

    def load_scenarios(self) -> List[Dict]:
        """Load all scenarios from database"""
        self._scenarios = fetch_all_scenarios_flat()
        return self._scenarios

    @property
    def scenarios(self) -> List[Dict]:
        """Get loaded scenarios (loads from DB if not already loaded)"""
        if not self._scenarios:
            self.load_scenarios()
        return self._scenarios

    def register_user(self, firstname: str, lastname: str, age: int,
                      krigsberedd: Optional[bool] = None) -> Optional[int]:
        """Register a new user and store their ID"""
        self._current_user_id = register_player(firstname, lastname, age, krigsberedd)
        return self._current_user_id

    @property
    def current_user_id(self) -> Optional[int]:
        return self._current_user_id

    @current_user_id.setter
    def current_user_id(self, user_id: int):
        self._current_user_id = user_id

    def save_choice(self, scenario_index: int, choice_label: str) -> bool:
        """
        Save a player's choice based on scenario index and choice label ('a', 'b', etc.)

        Args:
            scenario_index: Index of the current scenario in self. scenarios
            choice_label: The label of the choice ('a', 'b', etc.)

        Returns:
            True if successful
        """
        if not self._current_user_id or scenario_index >= len(self._scenarios):
            return False

        scenario = self._scenarios[scenario_index]

        # Find the choice by label
        choice = next(
            (c for c in scenario['choices'] if c['label'] == choice_label),
            None
        )

        if not choice:
            return False

        return record_player_choice(
            user_id=self._current_user_id,
            level_id=scenario['level_id'],
            scenario_id=scenario['id'],
            choice_id=choice['choice_id']
        )

    def get_user_results(self) -> Optional[Dict]:
        """Get current user's profile and attribute scores"""
        if not self._current_user_id:
            return None
        return get_player_profile(self._current_user_id)

    def refresh(self):
        """Reload scenarios from database"""
        self._scenarios = []
        self.load_scenarios()