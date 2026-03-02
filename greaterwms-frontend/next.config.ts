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

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8008",
  },
};

export default nextConfig;
