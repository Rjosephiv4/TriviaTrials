import os
from pathlib import Path
import tempfile
import unittest
from init_db import initialize


class AppSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.database = Path(cls.temp.name) / "test.db"
        initialize(cls.database)
        os.environ["TRIVIA_DATABASE"] = str(cls.database)
        os.environ["TRIVIA_SESSION_DIR"] = str(Path(cls.temp.name) / "sessions")
        os.environ["TRIVIA_SECRET_KEY"] = "local-test-only"
        os.environ.pop("TRIVIA_ENABLE_SCHEDULER", None)
        import app
        cls.module = app
        app.app.config.update(TESTING=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_existing_database_cannot_be_overwritten(self):
        with self.assertRaises(FileExistsError):
            initialize(self.database)

    def test_anonymous_pages_and_auth_boundary(self):
        with self.module.app.test_client() as client:
            for path in ("/", "/login", "/register", "/leaderboard"):
                self.assertEqual(client.get(path).status_code, 200, path)
            self.assertEqual(client.get("/getUserScores").status_code, 302)

    def test_registration_and_login_with_clean_database(self):
        with self.module.app.test_client() as client:
            result = client.post("/register", data={"email": "demo@example.com", "name": "Demo", "password": "TestPassword123", "confirm": "TestPassword123"})
            self.assertEqual(result.status_code, 302)
            self.assertEqual(client.get("/getUserScores").json["miniScoreToday"], 0)
            client.get("/logout")
            self.assertEqual(client.get("/getUserScores").status_code, 302)
            self.assertEqual(client.post("/login", data={"email": "demo@example.com", "paswrd": "TestPassword123"}).status_code, 302)
            self.assertEqual(client.get("/miniStart").status_code, 200)

    def test_import_does_not_start_scheduler(self):
        self.assertFalse(hasattr(self.module, "scheduler_thread"))
