import "./globals.scss";
import { Inter } from "next/font/google";

import AuthSession from "@/app/authSession";

import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
config.autoAddCss = false;

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "치직 - Chizik",
  description: '치지직 스트리머를 위한 디스코드 봇, "치직"',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body className={inter.className}>
        <AuthSession>{children}</AuthSession>
      </body>
    </html>
  );
}
