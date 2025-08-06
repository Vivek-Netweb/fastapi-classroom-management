
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    role VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


chat_messages
    no_of_tokens INT;

foreign key from chat_session
what is the name of latest llm 4    chat_session_id
latest is gemini 6
who is the developer 6
googlgev 4

chat_session
id
no of messages
total_no_of_tokens



user login 
chat_session :- fetch using user id 
chat_session :-> messages fetch using chat_session_id




-- query -> llm 
-- llm -> cache response :-> cost effective 
-- document upload, fir usko OCR text nikalenge and usko store 
-- llm -> text user details, 
-- cache -> response
