"use client";
import { getSession, signOut, useSession } from "next-auth/react";
import "./manage.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRefresh, faSignOut } from "@fortawesome/free-solid-svg-icons";
import { useEffect, useState } from "react";
import axios from "axios";
import Image from "next/image";
import Link from "next/link";

const validPermission = (1 << 3) | (1 << 5);

const checkForBot = async (guild) => {
  try {
    const res = await axios.get(`/api/chizik/guilds/${guild.id}`);
    guild.hasBot = res?.status === 200;
  } catch (err) {
    guild.hasBot = false;
  }
};

const Dashboard = ({ session }) => {
  const [userGuilds, setUserGuilds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/api/discord/v9/users/@me/guilds", {
        headers: {
          Authorization: `Bearer ${session.user.accessToken}`,
        },
      })
      .then(async (res) => {
        const guilds = res.data.filter(({ permissions }) => !!(Number.parseInt(permissions) & validPermission));

        await Promise.all(guilds.map(checkForBot));
        guilds.sort((a, b) => (a.hasBot != b.hasBot ? (a.hasBot ? -1 : 1) : a.name > b.name ? 1 : -1));
        setUserGuilds(guilds.filter(({ hasBot }) => hasBot));
      })
      .then(() => setLoading(false))
      .catch((err) => console.log(err));
  }, [session.user.accessToken]);

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
      <main className="Content">
        <br />
        <h1>서버 {userGuilds.length}개</h1>
        <div className="GuildList">
          {userGuilds.map((guild, index) => (
            <Link href={`/manage/${guild.id}`} key={index}>
              <div className="GuildItem" key={index}>
                <Image
                  className="GuildIcon"
                  alt="Guild Icon"
                  width="64"
                  height="64"
                  src={
                    guild.icon == null
                      ? "https://cdn.discordapp.com/embed/avatars/0.png"
                      : `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.webp?size=256`
                  }
                />
                <div>
                  <h2>{guild?.name}</h2>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </>
  );
};

export default Dashboard;
