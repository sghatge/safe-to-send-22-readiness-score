import json
import unittest

from readiness import DIMENSIONS, item_score, overall

with open("examples/profiles.json", encoding="utf-8") as fh:
    P = {p["name"]: p for p in json.load(fh)}


class ReadinessTest(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(w for _, w in DIMENSIONS.values()), 100)

    def test_item_scale(self):
        self.assertEqual(item_score(1), 0)
        self.assertEqual(item_score(5), 100)
        self.assertEqual(item_score(5, reverse=True), 0)

    def test_cap_applies(self):
        p = P["Fast mover, loose guardrails"]
        r = overall(p["answers"], p["flags"])
        self.assertTrue(r["capped"])
        self.assertEqual(r["score"], 59)
        self.assertGreater(r["raw"], 59)

    def test_no_flag_no_cap(self):
        p = P["Fast mover, loose guardrails"]
        self.assertFalse(overall(p["answers"], [])["capped"])


if __name__ == "__main__":
    unittest.main()
