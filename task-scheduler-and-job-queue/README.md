## Functional Requirements

- There can be 10 million jobs per day, ~50k jobs per min
- Jobs have 3 priroty status - high, medium, low
- Scheduler should be able to handle both cron jobs, and scheduled jobs
- No divide and conquer for now, only standard jobs
- Each job has a state and must be persisted in memory for reference
- Jobs should have maximum of 3 retries
- Handle duplicate jobs (duplicate payload) gracefully

## NFR

- Queue shall be available > 99.99% of time
- Maximum Job duration is 30 mins, after that it is timed out
- Jobs should be picked up based on priority (high < 1 min, medium < 5 min, low <10 min)
- If there is a spike, everything gets queued, and high priority gets done first
