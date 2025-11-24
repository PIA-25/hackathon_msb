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
    outcome_text   TEXT NOT NULL       -- feedback efter valet
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
    name           VARCHAR(50) NOT NULL,
    description    TEXT
);