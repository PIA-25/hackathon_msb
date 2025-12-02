-- Skapa tabell för användarresponser
CREATE TABLE IF NOT EXISTS user_responses (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    response_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index för snabbare sökning
CREATE INDEX IF NOT EXISTS idx_user_id ON user_responses(user_id);
CREATE INDEX IF NOT EXISTS idx_question ON user_responses(question);
CREATE INDEX IF NOT EXISTS idx_created_at ON user_responses(created_at);

-- Skapa tabell för frågorna
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT UNIQUE NOT NULL,
    description TEXT,
    answer_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exempelfråga
INSERT INTO questions (question_text, description, answer_type) 
VALUES ('Är du krigsbered?', 'En testfråga för att mäta krigsberördhet', 'multiple_choice')
ON CONFLICT DO NOTHING;
