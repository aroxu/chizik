"use client";
import { signIn, useSession } from "next-auth/react";
import "../../manage/manage.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRefresh, faSignIn } from "@fortawesome/free-solid-svg-icons";
import { redirect, useRouter } from "next/navigation";

const SignIn = () => {
  const { data: session, status } = useSession();
  const router = useRouter();

  if (session) {
    redirect("/manage");
  }

  return (
    <div className="ManageAuth">
      {status === "loading" ? (
        <>
          <FontAwesomeIcon className="LoadingIcon" icon={faRefresh} size="6x" />
          <br />
          <h4>로딩 중...</h4>
          <p>잠시만 기다려 주세요</p>
        </>
      ) : (
        <>
          <FontAwesomeIcon icon={faSignIn} size="6x" />
          <br />
          <p>계속하려면 Discord로 로그인 해주세요.</p>
          <div role="button" className="outline" onClick={() => signIn("discord")}>
            <span>로그인</span>
          </div>
          <br />
          <div role="button" className="contrast outline" onClick={() => router.replace("/")}>
            <span>메인페이지로 돌아가기</span>
          </div>
        </>
      )}
    </div>
  );
};

export default SignIn;
