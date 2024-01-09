import { signIn, useSession } from "next-auth/react";
import "./manage.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSignIn } from "@fortawesome/free-solid-svg-icons";
import Dashboard from "./dashboard";
import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/route";
import Link from "next/link";

const Manage = async () => {
  const session = await getServerSession(authOptions);

  if (session) {
    return (
      <div className="Manage">
        <Dashboard session={session} />
      </div>
    );
  }

  return (
    <div className="ManageAuth">
      <>
        <FontAwesomeIcon icon={faSignIn} size="6x" />
        <br />
        <p>계속하려면 Discord로 로그인 해주세요.</p>
        <div role="button" className="outline" onClick={() => signIn("discord")}>
          <span>로그인</span>
        </div>
        <br />
        <Link role="button" className="contrast outline" href="/">
          <span>메인페이지로 돌아가기</span>
        </Link>
      </>
    </div>
  );
};

export default Manage;
