CREATE TABLE users (
    user_id      SERIAL PRIMARY KEY,
    firstname    VARCHAR(50),
    lastname     VARCHAR(50),
    age          INT,
    krigsberedd  BOOLEAN,          -- true = ja, false = nej
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE TABLE levels (
    level_id      SERIAL PRIMARY KEY,
    level_number  INT NOT NULL,
    title         VARCHAR(100)
);

CREATE TABLE scenarios (
    scenario_id    SERIAL PRIMARY KEY,
    level_id       INT NOT NULL REFERENCES levels(level_id),
    scenario_text  TEXT NOT NULL
);

CREATE TABLE choice_options (
    choice_id      SERIAL PRIMARY KEY,
    scenario_id    INT NOT NULL REFERENCES scenarios(scenario_id),
    option_text    TEXT NOT NULL,      -- valet spelaren ser
    outcome_text   TEXT NOT NULL,      -- feedback efter valet
    is_good        BOOLEAN             -- true = bra val, false = dåligt val (kan vara NULL för neutrala val)
);

CREATE TABLE user_choices (
    user_choice_id  SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(user_id),
    level_id        INT NOT NULL REFERENCES levels(level_id),
    scenario_id     INT NOT NULL REFERENCES scenarios(scenario_id),
    choice_id       INT NOT NULL REFERENCES choice_options(choice_id),
    chosen_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE attributes (
    attribute_id   SERIAL PRIMARY KEY,
    name           VARCHAR(50) NOT NULL UNIQUE,
    description    TEXT
);

-- Kopplingstabell för relation mellan Users och Attributes
CREATE TABLE user_attributes (
    user_id        INT NOT NULL REFERENCES users(user_id),
    attribute_id   INT NOT NULL REFERENCES attributes(attribute_id),
    score          INT DEFAULT 0,  -- Poäng för detta attribut för denna användare
    PRIMARY KEY (user_id, attribute_id)
);

-- Kopplingstabell för relation mellan ChoiceOptions och Attributes
-- Varje val kan påverka flera attribut med olika poäng
CREATE TABLE choice_attributes (
    choice_id      INT NOT NULL REFERENCES choice_options(choice_id),
    attribute_id   INT NOT NULL REFERENCES attributes(attribute_id),
    score_change   INT NOT NULL,  -- Hur mycket detta val påverkar attributet (+ eller -)
    PRIMARY KEY (choice_id, attribute_id)
);
