import NextAuth, { NextAuthOptions } from "next-auth";
import DiscordProvider from "next-auth/providers/discord";

import { pages } from "@/config/pages";

const scopes = ["identify", "guilds"].join(" ");

const authOptions = {
  pages,
  providers: [
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID ?? "",
      clientSecret: process.env.DISCORD_CLIENT_SECRET ?? "",
      authorization: { params: { scope: scopes } },
    }),
  ],
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
