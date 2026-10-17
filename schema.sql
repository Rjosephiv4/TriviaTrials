CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE "leaderboard" (
    id INTEGER,
    playerName TEXT NOT NULL,
    miniScoreToday INTEGER NOT NULL,
    miniQuestionsToday INTEGER NOT NULL,
    miniScoreAllTime INTEGER NOT NULL,
    miniQuestionsAllTime INTEGER NOT NULL,
    classicScoreToday INTEGER NOT NULL,
    classicQuestionsToday INTEGER NOT NULL,
    classicScoreAllTime INTEGER NOT NULL,
    classicQuestionsAllTime INTEGER NOT NULL,
    classicPercentAllTime REAL GENERATED ALWAYS AS (
        CASE
            WHEN classicQuestionsAllTime != 0 THEN classicScoreAllTime * 1.0 / classicQuestionsAllTime
            ELSE 0
        END
    ) VIRTUAL,
    classicPercentToday REAL GENERATED ALWAYS AS (
        CASE
            WHEN classicQuestionsToday != 0 THEN classicScoreToday * 1.0 / classicQuestionsToday
            ELSE 0
        END
    ) VIRTUAL,
    miniPercentToday REAL GENERATED ALWAYS AS (
        CASE
            WHEN miniQuestionsToday != 0 THEN miniScoreToday * 1.0 / miniQuestionsToday
            ELSE 0
        END
    ) VIRTUAL,
    miniPercentAllTime REAL GENERATED ALWAYS AS (
        CASE
            WHEN miniQuestionsAllTime != 0 THEN miniScoreAllTime * 1.0 / miniQuestionsAllTime
            ELSE 0
        END
    ) VIRTUAL,
    FOREIGN KEY (id) REFERENCES users(id)
);
