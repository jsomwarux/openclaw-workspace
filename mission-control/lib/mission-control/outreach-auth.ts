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

export function assertServerCapability(provided: string | undefined, configured: string | undefined): void {
  if (!configured) throw new OutreachAuthError("server capability is not configured", 503);
  if (!provided || provided !== configured) throw new OutreachAuthError("server capability required", 401);
}
