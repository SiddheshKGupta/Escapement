#!/usr/bin/env python3
import argparse
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--task',required=True); p.add_argument('--goal',required=True); p.add_argument('--mode',choices=['FULL','DELTA','EXECUTE'],required=True); p.add_argument('--output',default='CURRENT_CONTEXT.md'); a=p.parse_args()
Path(a.output).write_text(f'# Context Pack\n- Task ID: {a.task}\n- Goal: {a.goal}\n- Mode: {a.mode}\n- Scope: TBD\n- Acceptance: TBD\n- Files: TBD\n- Skills: TBD\n- Checks: TBD\n'); print(a.output)
