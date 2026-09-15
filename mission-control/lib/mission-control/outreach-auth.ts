export class OutreachAuthError extends Error {
  constructor(message: string, readonly status: 401 | 503) {
    super(message);
  }
}

export function authorizeJtIdentity(headers: Headers, configuredLogin: string | undefined) {
  if (!configuredLogin) throw new OutreachAuthError("JT login is not configured", 503);
  const login = headers.get("Tailscale-User-Login");
  if (!login || login !== configuredLogin) throw new OutreachAuthError("JT identity required", 401);
  return { login };
}

function constantTimeEqual(left: string, right: string): boolean {
  const length = Math.max(left.length, right.length);
  let mismatch = left.length ^ right.length;
  for (let index = 0; index < length; index += 1) {
    mismatch |= (left.charCodeAt(index) || 0) ^ (right.charCodeAt(index) || 0);
  }
  return mismatch === 0;
}

export function assertDistinctServerCapability(
  provided: string | undefined,
  configured: string | undefined,
  peerConfigured: string | undefined,
): string {
  if (
    !configured?.trim()
    || !peerConfigured?.trim()
    || constantTimeEqual(configured, peerConfigured)
  ) {
    throw new OutreachAuthError("capability configuration is invalid", 503);
  }
  if (!provided?.trim() || !constantTimeEqual(provided, configured)) {
    throw new OutreachAuthError("server capability required", 401);
  }
  return configured;
}
