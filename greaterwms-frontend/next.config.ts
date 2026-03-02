import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export for Django integration
  output: "export",
  distDir: "out",

  // Trailing slashes to match Django URL patterns
  trailingSlash: true,

  // Image optimization disabled for static export
  images: {
    unoptimized: true,
  },

  // API URL resolved at runtime via api-client.ts (relative URLs)
};

export default nextConfig;
