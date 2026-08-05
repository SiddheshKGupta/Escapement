# Testing Standard

Use the smallest sufficient test pyramid:

```text
Static checks
→ Unit tests
→ Integration tests
→ Browser/end-to-end tests
→ UAT
```

Capture executed commands, exit codes, output paths, and hashes through
`scripts/run_check.py`.
