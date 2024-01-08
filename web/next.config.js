/** @type {import('next').NextConfig} */
const nextConfig = {
  swcMinify: true,
  compiler: {
    styledComponents: true,
  },
  rewrites: async () => [
    {
      source: "/api/chizik/:path*",
      destination: "http://chizik_bot:11020/:path*",
    },
  ],
};

module.exports = nextConfig;
