import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Keep local verification builds from clobbering the live `next dev` cache.
  distDir: process.env.NEXT_DIST_DIR || ".next",
  // Allow reading files from ~/.openclaw for the API routes
  serverExternalPackages: [],
};

export default nextConfig;
