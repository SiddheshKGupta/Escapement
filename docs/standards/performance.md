# Performance Standard

## Target

Measure. Do not claim.

Preferred: Lighthouse 90+ where realistic.

## Frontend

- split code
- lazy load
- optimise image/font
- virtualise large lists
- paginate
- cache
- cancel stale request
- skeleton
- optimistic UI only when reversible

## Network

- compress useful text payloads
- batch safe writes
- avoid N+1
- parallel independent calls
- cache reference data
- aggregate endpoints

## Scale

Start simple. Record trigger for:

- bigger instance
- more workers
- read replica
- queue
- distributed cache
- partition/shard

No premature complexity.
