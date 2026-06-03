import unittest

from fastapi.testclient import TestClient

from app.main import app


class TestMCPAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_health(self) -> None:
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_pricing_overview_shape(self) -> None:
        response = self.client.get("/api/v1/pricing-overview")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertIn("today_market_price", payload)
        self.assertIn("prediction_7_days", payload)
        self.assertIn("factory_storage", payload)
        self.assertIn("active_logistics", payload)
        self.assertEqual(len(payload["prediction_7_days"]), 7)


if __name__ == "__main__":
    unittest.main()
