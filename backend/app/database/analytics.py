from sqlalchemy import func, case
from .database import SessionLocal
from .models import UserChoice, ChoiceOption, User, Attribute, user_attributes


def get_choice_overview():
    """Returns choice statistics per scenario"""
    try:
        with SessionLocal() as db:
            rows = (
                db.query(
                    UserChoice.scenario_id,
                    func.count().label('total'),
                    func.sum(case((ChoiceOption.is_good.is_(True), 1), else_=0)).label('good'),
                    func.sum(case((ChoiceOption.is_good.is_(False), 1), else_=0)).label('bad'),
                )
                .join(ChoiceOption, ChoiceOption.choice_id == UserChoice.choice_id)
                .group_by(UserChoice.scenario_id)
                .order_by(UserChoice.scenario_id)
                .all()
            )
            return [
                {'scenario': row.scenario_id, 'good': row.good or 0, 'bad': row.bad or 0}
                for row in rows
            ]
    except Exception as e:
        print(f"Error in get_choice_overview: {e}")
        return []


def get_age_behavior():
    """Returns choice behavior grouped by age bands"""
    try:
        with SessionLocal() as db:
            rows = (
                db.query(
                    (func.floor(User.age / 10) * 10).label('age_band'),
                    ChoiceOption.is_good,
                    func.count().label('cnt'),
                )
                .join(UserChoice, UserChoice.user_id == User.user_id)
                .join(ChoiceOption, ChoiceOption.choice_id == UserChoice.choice_id)
                .group_by('age_band', ChoiceOption.is_good)
                .order_by('age_band')
                .all()
            )
            return [
                {
                    'age_band': int(row.age_band or 0),
                    'is_good': True if row.is_good else False if row.is_good is not None else None,
                    'count': row.cnt,
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Error in get_age_behavior: {e}")
        return []


def get_attribute_impacts():
    """Returns total attribute scores across all users"""
    try:
        with SessionLocal() as db:
            rows = (
                db.query(
                    Attribute.name,
                    func.sum(user_attributes.c.score).label('score'),
                )
                .join(user_attributes, user_attributes.c.attribute_id == Attribute.attribute_id)
                .group_by(Attribute.name)
                .order_by(func.sum(user_attributes.c.score).desc())
                .all()
            )
            return [{'name': row.name, 'score': row.score or 0} for row in rows]
    except Exception as e:
        print(f"Error in get_attribute_impacts: {e}")
        return []