import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
cases = json.loads((root / "evals" / "evals.json").read_text())["cases"]
failures = []

if len(cases) != 5:
    failures.append(f"expected 5 cases, found {len(cases)}")

for case in cases:
    skill = root / "skills" / case["skill"] / "SKILL.md"
    if not skill.is_file():
        failures.append(f"{case['id']}: missing {skill.relative_to(root)}")
        continue
    text = skill.read_text()
    for needle in case["skill_must_contain"]:
        if needle not in text:
            failures.append(f"{case['id']}: {case['skill']} lacks {needle!r}")

skill_dirs = sorted(p.name for p in (root / "skills").iterdir() if p.is_dir())
if not 4 <= len(skill_dirs) <= 5:
    failures.append(f"expected 4 or 5 skills, found {skill_dirs}")

for name in skill_dirs:
    head = (root / "skills" / name / "SKILL.md").read_text().split("---")[1]
    if f"name: {name}" not in head or "description:" not in head:
        failures.append(f"{name}: frontmatter needs name and description")

for line in failures:
    print("FAIL", line)
if not failures:
    print(f"evals ok: {len(cases)} cases, {len(skill_dirs)} skills")
sys.exit(1 if failures else 0)
