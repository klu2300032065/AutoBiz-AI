interface RateLimitRecord {
  count: number;
  firstRequestTime: number;
}

const rateLimitMap = new Map<string, RateLimitRecord>();

// Clean up stale entries every 15 minutes
setInterval(() => {
  const now = Date.now();
  for (const [key, value] of rateLimitMap.entries()) {
    if (now - value.firstRequestTime > 15 * 60 * 1000) {
      rateLimitMap.delete(key);
    }
  }
}, 15 * 60 * 1000);

/**
 * Checks if a given IP has exceeded max submissions within a given window.
 * Default: 5 requests per 10 minutes.
 */
export function checkRateLimit(
  ip: string,
  limit = 5,
  windowMs = 10 * 60 * 1000
): { allowed: boolean; remaining: number } {
  const now = Date.now();
  const record = rateLimitMap.get(ip);

  if (!record) {
    rateLimitMap.set(ip, { count: 1, firstRequestTime: now });
    return { allowed: true, remaining: limit - 1 };
  }

  if (now - record.firstRequestTime > windowMs) {
    rateLimitMap.set(ip, { count: 1, firstRequestTime: now });
    return { allowed: true, remaining: limit - 1 };
  }

  if (record.count >= limit) {
    return { allowed: false, remaining: 0 };
  }

  record.count += 1;
  return { allowed: true, remaining: limit - record.count };
}
