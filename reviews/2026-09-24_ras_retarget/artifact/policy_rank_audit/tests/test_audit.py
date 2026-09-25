import csv
import json
import math
import tempfile
import unittest
from pathlib import Path

from policy_rank_audit.core import AuditInputError, allocate, audit_csv, directional_iut, holm_adjust


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manifest = {
            "schema_version":1,
            "metadata":{"build":"synthetic-test-build","estimand":"equal_configuration_mean_success_difference",
                        "replicate_unit":"complete_independent_census_run","independent_runs":True,
                        "independent_policy_evaluations":True},
            "tasks":{"toy":{"policies":["A","B"],"conditions":["nominal","stress"],
                            "configurations":["c0","c1","c2","c3"],"replicates":["r0","r1"]}}}
        self.rows = []
        # A run means [1,0], B run means [0,0.5]; uncertainty must use n=2 runs.
        for p,counts in (("A",[4,0]),("B",[0,2])):
            for cond in ["nominal","stress"]:
                for r,k in enumerate(counts):
                    for c in range(4):
                        self.rows.append(dict(task="toy",policy=p,condition=cond,configuration=f"c{c}",
                                              replicate=f"r{r}",success=int(c<k)))

    def tearDown(self):
        self.temp.cleanup()

    def run_audit(self,rows=None,manifest=None):
        manifest = self.manifest if manifest is None else manifest
        rows = self.rows if rows is None else rows
        csv_path,plan_path = self.root/"data.csv",self.root/"manifest.json"
        with csv_path.open("w",newline="",encoding="utf-8") as stream:
            writer=csv.DictWriter(stream,fieldnames=["task","policy","condition","configuration","replicate","success"])
            writer.writeheader();writer.writerows(rows)
        plan_path.write_text(json.dumps(manifest),encoding="utf-8")
        return audit_csv(csv_path,plan_path)

    def test_complete_census_run_is_the_variance_unit(self):
        result=self.run_audit()
        self.assertTrue(result["coverage"][0]["complete_inventory"])
        pair=result["pairs"][0]
        self.assertTrue(pair["eligible"])
        self.assertAlmostEqual(pair["conditions"][0]["gap"],.25)
        self.assertAlmostEqual(pair["conditions"][0]["standard_error"],math.sqrt(.3125))
        self.assertEqual(pair["conditions"][0]["runs_a"],2)

    def test_missing_cell_never_yields_complete_envelope(self):
        result=self.run_audit(self.rows[:-1])
        self.assertFalse(result["coverage"][0]["complete_inventory"])
        self.assertIsNone(result["pairs"][0]["envelope"])
        self.assertEqual(result["pairs"][0]["holm_verdict"],"abstain_unsupported")
        self.assertTrue(all(c["interval"] is None for c in result["pairs"][0]["conditions"]))

    def test_duplicate_rows_cannot_supply_extra_repeats(self):
        with self.assertRaisesRegex(AuditInputError,"duplicate observation"):
            self.run_audit(self.rows+[self.rows[0].copy()])

    def test_unplanned_run_ids_are_rejected(self):
        rows=[dict(r) for r in self.rows]
        rows[0]["replicate"]="episode_99"
        with self.assertRaisesRegex(AuditInputError,"replicate not in"):
            self.run_audit(rows)

    def test_one_run_descriptive_only_even_with_many_configurations(self):
        self.manifest["tasks"]["toy"]["replicates"]=["r0"]
        result=self.run_audit([r for r in self.rows if r["replicate"]=="r0"])
        self.assertTrue(result["coverage"][0]["complete_inventory"])
        self.assertIsNone(result["pairs"][0]["envelope"])
        self.assertIn("fewer_than_two_independent_census_runs",result["pairs"][0]["unsupported_reasons"])

    def test_zero_empirical_variance_is_not_certainty(self):
        rows=[dict(r,success=int(r["policy"]=="A")) for r in self.rows]
        result=self.run_audit(rows)
        self.assertIsNone(result["pairs"][0]["envelope"])
        self.assertEqual(result["pairs"][0]["raw_p"],1)

    def test_declared_dependence_prevents_independent_policy_interval(self):
        self.manifest["metadata"]["independent_policy_evaluations"]=False
        result=self.run_audit()
        self.assertIsNone(result["pairs"][0]["envelope"])

    def test_configuration_identifier_is_not_an_independent_run(self):
        self.manifest["metadata"]["replicate_unit"]="episode"
        with self.assertRaisesRegex(AuditInputError,"complete independent census"):
            self.run_audit()

    def test_mixed_direction_iut_does_not_use_small_two_sided_pvalues(self):
        result=directional_iut([2,-2],[.1,.1])
        self.assertEqual(result["two_direction_p"],1)
        self.assertLess(directional_iut([2,2],[.1,.1])["two_direction_p"],1e-20)

    def test_holm_includes_unsupported_pairs_in_family(self):
        self.assertEqual(holm_adjust([.01,.04,.2,1]),[.04,.12,.4,1])

    def test_neyman_continuous_cost_constraint_and_local_optimum(self):
        result=allocate({"budget":100,"strata":[{"id":"a","weight":.5,"sigma":.2,"cost":1},
                                                  {"id":"b","weight":.5,"sigma":.4,"cost":4}]})
        self.assertAlmostEqual(result["allocated_cost"],100)
        self.assertAlmostEqual(result["strata"][0]["continuous_runs"],20)
        self.assertAlmostEqual(result["strata"][1]["continuous_runs"],20)
        self.assertLess(result["model_predicted_variance"],.1**2/24+.2**2/19)
        self.assertLess(result["model_predicted_variance"],.1**2/16+.2**2/21)

    def test_allocation_rejects_uninformative_pilot_and_invalid_weights(self):
        for weights,sigmas in (([.5,.5],[0,0]),([1,1],[.1,.2])):
            with self.assertRaises(AuditInputError):
                allocate({"budget":100,"strata":[{"id":str(i),"weight":weights[i],"sigma":sigmas[i],"cost":1} for i in range(2)]})


if __name__ == "__main__":
    unittest.main()
