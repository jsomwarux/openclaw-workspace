import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Allow reading files from ~/.openclaw for the API routes
  serverExternalPackages: [],
};

export default nextConfig;
