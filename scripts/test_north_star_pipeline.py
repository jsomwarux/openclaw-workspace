import unittest

import north_star_pipeline as pipeline


class NorthStarSummaryTests(unittest.TestCase):
    def test_extract_revenue_metrics_reads_mission_control_payload(self):
        payload = {
            "metrics": {
                "consultingCollected": 1250,
                "weightedForecast": 3750,
            }
        }

        self.assertEqual(
            pipeline.extract_revenue_metrics(payload),
            {"consultingCollected": 1250, "weightedForecast": 3750},
        )

    def test_summary_uses_live_revenue_metrics_instead_of_legacy_constants(self):
        metrics = {
            "consultingCollected": 0,
            "weightedForecast": 0,
        }

        result = pipeline.summary([], revenue_metrics=metrics)

        self.assertEqual(result["current_collected"], 0)
        self.assertEqual(result["weighted_forecast"], 0)
        self.assertEqual(result["gap_to_10k_collected"], 10000)
        self.assertEqual(result["gap_to_10k_with_forecast"], 10000)
        self.assertEqual(result["revenue_source"], "mission_control_api")


if __name__ == "__main__":
    unittest.main()
