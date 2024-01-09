import NextAuth from "next-auth";
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
  callbacks: {
    async session({ session, token }) {
      session.user.id = token.id;
      session.user.locale = token.locale;
      session.user.discriminator = token.discriminator;
      session.user.accessToken = token.accessToken;
      return Promise.resolve(session);
    },
    async jwt({ token, account, profile }) {
      if (account) {
        token.accessToken = account.access_token;
      }
      if (profile) {
        token.id = profile.id;
        token.locale = profile.locale;
        token.discriminator = profile.discriminator;
      }
      return Promise.resolve(token);
    },
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST, authOptions };
