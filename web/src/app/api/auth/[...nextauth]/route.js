import NextAuth from "next-auth";
import DiscordProvider from "next-auth/providers/discord";

const scopes = ["identify", "guilds"].join(" ");

const handler = NextAuth({
  pages: {
    signIn: "/manage/auth/error",
    error: "/manage/auth/error",
  },
  providers: [
    DiscordProvider({
      clientId: process.env.DISCORD_CLIENT_ID ?? "",
      clientSecret: process.env.DISCORD_CLIENT_SECRET ?? "",
      authorization: { params: { scope: scopes } },
    }),
  ],
});

export { handler as GET, handler as POST };
