ALTER TABLE chat_history
ADD COLUMN title TEXT,
ADD COLUMN explanation TEXT,
ADD COLUMN points JSONB;
