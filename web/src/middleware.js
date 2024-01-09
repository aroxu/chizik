import { withAuth } from "next-auth/middleware";

import { pages } from "./config/pages";

export default withAuth({
  pages,
});

export const config = {
  matcher: ["/manage/:path*", "/api/:path*"],
};
