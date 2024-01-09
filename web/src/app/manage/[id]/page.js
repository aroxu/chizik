"use client";
import "./page.scss";
import { faRefresh, faSignOut } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { signOut, useSession } from "next-auth/react";
import { useEffect, useState } from "react";

export default function ManageGuild({ params }) {
  const { id } = params;
  const { data: session, status } = useSession();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (status === "loading") return;

    if (status === "authenticated") {
      setLoading(false);
    }
  }, [status]);

  if (loading) {
    return (
      <div className="Loading">
        <FontAwesomeIcon className="LoadingIcon" icon={faRefresh} size="6x" />
        <br />
        <h4>로드 중...</h4>
        <p>잠시만 기다려 주세요</p>
      </div>
    );
  }

  return (
    <>
      <header className="Header">
        <nav className="Nav">
          <h2>관리</h2>
          <div className="NavActions">
            <span>
              <b>{session.user.name}</b> 로 로그인 됨
            </span>
            <div role="button" className="SignOutButton outline" onClick={() => signOut()}>
              <FontAwesomeIcon icon={faSignOut} size="1x" /> <span>로그아웃</span>
            </div>
          </div>
        </nav>
      </header>
      <main className="ManageGuild">
        <div>
          <h1>{id}</h1>
        </div>
      </main>
    </>
  );
}
