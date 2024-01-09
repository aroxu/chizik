/** @type {import('next').NextConfig} */
const nextConfig = {
  swcMinify: true,
  compiler: {
    styledComponents: true,
  },
  rewrites: async () => [
    {
      source: "/api/chizik/:path*",
      destination: `http://${process.env.API_HOST}:${process.env.API_PORT}/:path*`,
    },
    {
      source: "/api/discord/:path*",
      destination: "https://discord.com/api/:path*",
    },
  ],
  images: {
    domains: ["cdn.discordapp.com"],
  },
};

module.exports = nextConfig;

// TODO: remove rewrites adn use custom api with next-auth
