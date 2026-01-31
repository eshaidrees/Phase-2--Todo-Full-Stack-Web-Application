import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    serverActions: true,
  },
  // Prevents SSR and hydration issues
  reactStrictMode: true,
  swcMinify: true,
};

export default nextConfig;
