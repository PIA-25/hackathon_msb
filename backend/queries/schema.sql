
CREATE TABLE users (
    user_id          SERIAL PRIMARY KEY,
    username         VARCHAR(50),
    gender           VARCHAR(50),
    age              INT,
    occupation       VARCHAR(50),
    leadership_style  VARCHAR(50),
    priority         VARCHAR(50),
    team_role        VARCHAR(50),
    risk_tolerance   VARCHAR(50),
    created_at       TIMESTAMP DEFAULT NOW()
);

-- Create indexes for users table
CREATE INDEX IF NOT EXISTS ix_users_user_id ON users(user_id);
CREATE INDEX IF NOT EXISTS ix_users_age ON users(age);

CREATE TABLE levels (
    level_id      SERIAL PRIMARY KEY,
    level_number  INT NOT NULL,
    title         VARCHAR(100)
);

-- Create indexes for levels table
CREATE INDEX IF NOT EXISTS ix_levels_level_id ON levels(level_id);

CREATE TABLE scenarios (
    scenario_id    SERIAL PRIMARY KEY,
    level_id       INT NOT NULL REFERENCES levels(level_id) ON DELETE CASCADE,
    scenario_text  TEXT NOT NULL
);

-- Create indexes for scenarios table
CREATE INDEX IF NOT EXISTS ix_scenarios_scenario_id ON scenarios(scenario_id);
CREATE INDEX IF NOT EXISTS ix_scenarios_level_id ON scenarios(level_id);

CREATE TABLE choice_options (
    choice_id      SERIAL PRIMARY KEY,
    scenario_id    INT NOT NULL REFERENCES scenarios(scenario_id) ON DELETE CASCADE,
    option_text    TEXT NOT NULL,      -- valet spelaren ser
    outcome_text   TEXT NOT NULL,      -- feedback efter valet
    is_good        BOOLEAN             -- true = bra val, false = dåligt val (kan vara NULL för neutrala val)
);

-- Create indexes for choice_options table
CREATE INDEX IF NOT EXISTS ix_choice_options_choice_id ON choice_options(choice_id);
CREATE INDEX IF NOT EXISTS ix_choice_options_scenario_id ON choice_options(scenario_id);

CREATE TABLE user_choices (
    user_choice_id  SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    level_id        INT NOT NULL REFERENCES levels(level_id) ON DELETE CASCADE,
    scenario_id     INT NOT NULL REFERENCES scenarios(scenario_id) ON DELETE CASCADE,
    choice_id       INT NOT NULL REFERENCES choice_options(choice_id) ON DELETE CASCADE,
    chosen_at       TIMESTAMP DEFAULT NOW()
);

-- Create indexes for user_choices table
CREATE INDEX IF NOT EXISTS ix_user_choices_user_choice_id ON user_choices(user_choice_id);
CREATE INDEX IF NOT EXISTS ix_user_choices_user_id ON user_choices(user_id);
CREATE INDEX IF NOT EXISTS ix_user_choices_level_id ON user_choices(level_id);
CREATE INDEX IF NOT EXISTS ix_user_choices_scenario_id ON user_choices(scenario_id);
CREATE INDEX IF NOT EXISTS ix_user_choices_choice_id ON user_choices(choice_id);

CREATE TABLE attributes (
    attribute_id   SERIAL PRIMARY KEY,
    name           VARCHAR(50) NOT NULL UNIQUE,
    description    TEXT
);

-- Create indexes for attributes table
CREATE INDEX IF NOT EXISTS ix_attributes_attribute_id ON attributes(attribute_id);

-- Kopplingstabell för relation mellan Users och Attributes
CREATE TABLE user_attributes (
    user_id        INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    attribute_id   INT NOT NULL REFERENCES attributes(attribute_id) ON DELETE CASCADE,
    score          INT DEFAULT 0,  -- Poäng för detta attribut för denna användare
    PRIMARY KEY (user_id, attribute_id)
);

-- Create indexes for user_attributes table
CREATE INDEX IF NOT EXISTS ix_user_attributes_user_id ON user_attributes(user_id);
CREATE INDEX IF NOT EXISTS ix_user_attributes_attribute_id ON user_attributes(attribute_id);

-- Kopplingstabell för relation mellan ChoiceOptions och Attributes
-- Varje val kan påverka flera attribut med olika poäng
CREATE TABLE choice_attributes (
    choice_id      INT NOT NULL REFERENCES choice_options(choice_id) ON DELETE CASCADE,
    attribute_id   INT NOT NULL REFERENCES attributes(attribute_id) ON DELETE CASCADE,
    score_change   INT NOT NULL,  -- Hur mycket detta val påverkar attributet (+ eller -)
    PRIMARY KEY (choice_id, attribute_id)
);

-- Create indexes for choice_attributes table
CREATE INDEX IF NOT EXISTS ix_choice_attributes_choice_id ON choice_attributes(choice_id);
CREATE INDEX IF NOT EXISTS ix_choice_attributes_attribute_id ON choice_attributes(attribute_id);
