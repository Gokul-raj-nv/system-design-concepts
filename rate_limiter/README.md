# Token Bucket Rate Limiter

## 1. Overview

Implemented a basic API Rate Limiter using the **Token Bucket Algorithm** in Python.

A rate limiter controls the number of requests a user can make within a given period. The Token Bucket algorithm allows requests at a controlled average rate while supporting short bursts of traffic.

Each user is assigned an independent token bucket. A request is allowed only when the user's bucket contains at least one token.

## 2. Token Bucket Algorithm

The algorithm works using three fundamental rules:

1. **Bucket Capacity:** Each bucket has a maximum token capacity.
2. **Token Refill:** Tokens are replenished continuously at a predefined refill rate.
3. **Token Consumption:** Each incoming request consumes one token. If no tokens are available, the request is rejected.

### Configuration

| Parameter | Value |
|---|---:|
| Bucket Capacity | 5 tokens |
| Refill Rate | 2 tokens/second |
| Initial Tokens | 5 |
| Cost per Request | 1 token |

## 3. Data Structure

A Python Dictionary (Hash Map) is used to maintain independent token buckets for multiple users.

**Structure:**

- Key: User ID
- Value: Dictionary containing:
  - `tokens`: Currently available tokens.
  - `last_refill`: Timestamp of the last refill calculation.

Conceptually:

```text
user_buckets = {
    user_101: {
        tokens: 4,
        last_refill: timestamp
    },
    user_102: {
        tokens: 2,
        last_refill: timestamp
    }
}
```

This approach provides efficient average O(1) lookup and update operations.

## 4. Algorithm Workflow

For every incoming request:

1. Identify the user using their unique user ID.
2. Check whether the user already has a bucket.
3. If the bucket does not exist, initialize it with the maximum token capacity.
4. Retrieve the user's bucket state.
5. Calculate the elapsed time since the previous refill calculation.
6. Calculate the newly generated tokens using the refill rate.
7. Update the token count without exceeding the bucket capacity.
8. Update the last refill timestamp.
9. If at least one token is available:
   - Consume one token.
   - Allow the request.
10. Otherwise, reject the request.

### Token Refill Formula

Let:

- C = Maximum bucket capacity
- r = Refill rate
- Δt = Elapsed time
- B = Previously available tokens

The updated token count is:

\[
B_{new} = \min(C,\ B+r\Delta t)
\]

### Request Validation

\[
Request =
\begin{cases}
Allowed, & B_{new} \geq 1\\
Rejected, & B_{new} < 1
\end{cases}
\]

If allowed, one token is deducted from the bucket.

## 5. Implementation Details

**Technologies:**
- Python
- Dictionary (Hash Map)
- `time.monotonic()` for measuring elapsed time

**Key Implementation Concepts:**

- Lazy Token Refill: Tokens are calculated when a request arrives instead of using a continuously running background refill process.
- Independent User Buckets: Each user maintains a separate token count and refill timestamp.
- Capacity Enforcement: The `min()` operation ensures that the bucket never exceeds its maximum capacity.
- Time-Based Replenishment: The refill rate determines how quickly request capacity is restored.

## 6. Complexity Analysis

| Operation | Time Complexity |
|---|---|
| Hash Map Lookup | O(1) average |
| Token Refill Calculation | O(1) |
| Token Consumption | O(1) |
| Hash Map Update | O(1) average |

**Overall Time Complexity:** O(1) average per request.

**Space Complexity:** O(N), where N is the number of users with stored bucket states.



This is a basic sequential implementation intended to understand the Token Bucket algorithm.

The current implementation does not handle:

- Concurrent requests and race conditions.
- Atomic token consumption.
- Cleanup of inactive user buckets.
- Distributed rate limiting across multiple application servers.

These limitations will be addressed through subsequent extensions.

