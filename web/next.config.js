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
    {
      source: "/api/discord/:path*",
      destination: "https://discord.com/api/:path*",
    },
  ],
};

module.exports = nextConfig;

// TODO: remove rewrites adn use custom api with next-auth
