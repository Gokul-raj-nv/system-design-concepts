import time


class TokenBucket:
    def __init__(self, tokens, fill_rate):
        self.tokens = tokens
        self.fill_rate = fill_rate

        self.user_bucket = {}

    def allow_request(self, user_id):

        current_time = time.monotonic()

        if user_id not in self.user_bucket:
            self.user_bucket[user_id] = {
                "tokens" : self.tokens,
                "last_refill" : current_time
            }

        bucket = self.user_bucket[user_id]

        elapsed = current_time - bucket["last_refill"]

        new_tokens = self.fill_rate * elapsed

        bucket["tokens"] = min(self.tokens, bucket["tokens"] + new_tokens)

        bucket["last_refill"] = current_time


        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else :
            return False


rate_limiter = TokenBucket(
    tokens = 5,
    fill_rate = 2
)

requests = [
    "user_101",
    "user_101",
    "user_101",
    "user_101",
    "user_101",
    "user_101",
    "user_101",
    "user_102",
]

for user in requests:
    if rate_limiter.allow_request(user):
        print(f"{user}: Request Allowed")
    else:
        print(f"{user}: Request Rejected")




