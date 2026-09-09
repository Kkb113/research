# Completed external validation

GitHub Actions run: https://github.com/Kkb113/research/actions/runs/34353180786

Executed source commit: `a2c04034a4ddb46ebf84b0e8a2ea286ee8c4eb2a`.
Protocol commit: `63fe419288d8cc79b1af120a707c2ec3bed2dee5`.
Upstream: `4accc199a55695ebbefaab4fb6a99faa800fcabf`.
Artifact ID: `10104696349`, name `e2-clean-machine-evidence`.
Artifact SHA256: `8ceca60fe132c6e7e74c905c33238a44096bcfc685dbd82db18820dfb5602772`.

The workflow verifies frozen helper-file SHA256 values, reacquires all 112 original public inputs, runs nine unit/oracle tests, executes 2,480 finite-corpus configuration comparisons, the real extraction-stage mirror and original loader, corrected RSS measurements, and serialization stress. The artifact was downloaded and its numerical outputs inspected, not inferred from a green status alone.

Local versus external checks:

- 2,480 saved comparison dictionaries identical, including output digests.
- 155 saved arrays identical (five arrays for each of 31 primary selections).
- All four extraction-volume output hash sets and counts identical.
- Metadata agrees after removing only the local mirror's transport URL, whose port necessarily differs; metadata was identical between all arms within each run.
- All six serialization workload/method array-hash sets identical.
- Published frozen algorithm source bytes match the local files exactly.

External whole-stage median seconds, upstream / sparse / block / stream:

| Volume | Upstream | Sparse | Block | Stream |
|---|---:|---:|---:|---:|
| PHerc0332 | 0.1968 | 0.1627 | 0.1220 | 0.1449 |
| PHerc1299 | 0.1304 | 0.1174 | 0.1126 | 0.1148 |
| PHerc0139 | 0.2183 | 0.2093 | 0.1950 | 0.1979 |
| PHercParis4 | 0.2205 | 0.2103 | 0.1905 | 0.1926 |

At 17,279,232 repeated-real records, external concatenate/stream VmHWM is 330.9766/39.0898 MiB; elapsed time is 17.0097/17.1882 seconds. Timing need not match local timing. Resource and source snapshots are retained in the artifact and delivered archive.

This is computational reproduction on a second CPU environment, not independent scientific replication, expert validation, a GPU reconstruction run or upstream acceptance. Temporary artifact expiry does not prevent reacquisition/re-execution from committed provenance.
