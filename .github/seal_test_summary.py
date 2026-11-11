#!/usr/bin/env python3
"""Print per-suite surefire results, a total, and every skipped test with its reason."""
import glob
import sys
import xml.etree.ElementTree as ET

files = sorted(glob.glob("*/target/surefire-reports/TEST-*.xml"))
if not files:
    print("SEAL TEST SUMMARY: no surefire reports found")
    sys.exit(1)
tot = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
skipped = []
for path in files:
    root = ET.parse(path).getroot()
    counts = {k: int(root.get(k, "0") or 0) for k in tot}
    for k in tot:
        tot[k] += counts[k]
    print("SUITE %s: tests=%d failures=%d errors=%d skipped=%d" % (
        root.get("name"), counts["tests"], counts["failures"], counts["errors"], counts["skipped"]))
    for tc in root.iter("testcase"):
        sk = tc.find("skipped")
        if sk is not None:
            msg = sk.get("message") or (sk.text or "").strip() or "(no message)"
            skipped.append("%s.%s -- reason: %s" % (tc.get("classname"), tc.get("name"), msg))
passed = tot["tests"] - tot["failures"] - tot["errors"] - tot["skipped"]
print("SEAL TEST SUMMARY: Tests run: %d, Passed: %d, Failures: %d, Errors: %d, Skipped: %d" % (
    tot["tests"], passed, tot["failures"], tot["errors"], tot["skipped"]))
for s in skipped:
    print("SKIPPED: " + s)
sys.exit(1 if tot["failures"] or tot["errors"] else 0)
