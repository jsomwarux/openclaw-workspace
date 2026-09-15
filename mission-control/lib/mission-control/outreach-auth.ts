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

const CAPABILITY_COMPARISON_CONTEXT = new TextEncoder().encode("mission-control/outreach-capability/v1");

/**
 * Compare secrets through the platform Web Crypto implementation. HMAC-SHA-256
 * produces a fixed-length authenticator and `verify` performs the sensitive
 * comparison inside the cryptographic primitive rather than in JavaScript.
 * This works in both the Next.js and Convex runtimes.
 */
export async function secureCapabilityEqual(left: string, right: string): Promise<boolean> {
  const algorithm = { name: "HMAC", hash: "SHA-256" } as const;
  const encoder = new TextEncoder();
  const [leftKey, rightKey] = await Promise.all([
    crypto.subtle.importKey("raw", encoder.encode(left), algorithm, false, ["sign"]),
    crypto.subtle.importKey("raw", encoder.encode(right), algorithm, false, ["verify"]),
  ]);
  const authenticator = await crypto.subtle.sign("HMAC", leftKey, CAPABILITY_COMPARISON_CONTEXT);
  return crypto.subtle.verify("HMAC", rightKey, authenticator, CAPABILITY_COMPARISON_CONTEXT);
}

export async function assertDistinctServerCapability(
  provided: string | undefined,
  configured: string | undefined,
  peerConfigured: string | undefined,
): Promise<string> {
  if (
    !configured?.trim()
    || !peerConfigured?.trim()
  ) {
    throw new OutreachAuthError("capability configuration is invalid", 503);
  }
  if (await secureCapabilityEqual(configured, peerConfigured)) {
    throw new OutreachAuthError("capability configuration is invalid", 503);
  }
  if (!provided?.trim() || !(await secureCapabilityEqual(provided, configured))) {
    throw new OutreachAuthError("server capability required", 401);
  }
  return configured;
}
