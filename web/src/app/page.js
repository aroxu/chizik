"use client";
import Image from "next/image";
import "./page.scss";
import Link from "next/link";

const preventRightClick = (event) => {
  event.preventDefault();
};

export default function Home() {
  return (
    <main className="App">
      <div className="App-container">
        <div className="App-left">
          <div className="App-content">
            <Image
              src="/logo.png"
              width={0}
              height={0}
              sizes="25vmin"
              className="App-logo"
              alt="logo"
              onContextMenu={preventRightClick}
            />
            <h3>치지직 스트리머를 위한 디스코드 봇, "치직"</h3>

            <div className="Menus">
              <Link
                href="https://discord.com/oauth2/authorize?client_id=1183664649418326079&scope=bot+applications.commands&permissions=149504"
                role="button"
                className="outline"
              >
                초대하기
              </Link>
              <Link href="/manage" role="button" className="outline">
                관리하기
              </Link>
            </div>

            <br />
            <Link href="https://discord.gg/3cr7mduVh4" role="button" className="contrast outline">
              치직 봇 지원 서버
            </Link>
            <br />
            <p>
              <Link href="https://toss.me/aroxu" target="_blank" rel="noreferrer">
                <span>개발자 도와주기</span>
              </Link>
            </p>
          </div>
        </div>
        <div className="App-right">
          <div className="App-content">
            <Image
              src="/screenshots/screenshot_1.png"
              width={0}
              height={0}
              sizes="50vmin"
              alt="디스코드 방송 알림"
              className="Screenshot"
              onContextMenu={preventRightClick}
            />

            <br />
            <h2>디스코드에 방송 알림을 바로 보내보세요.</h2>
            <p>나의 시청자들에게 쉽게 알림을 전송할 수 있습니다.</p>
          </div>
          <div className="App-content">
            <Image
              src="/screenshots/screenshot_2.png"
              width={0}
              height={0}
              sizes="50vmin"
              alt="방송 정보 조회"
              className="Screenshot"
              onContextMenu={preventRightClick}
            />
            <br />
            <h2>채널 정보 조회하기</h2>
            <p>누적 시청자 수, 현재 시청자 수 등 채널 정보를 쉽게 확인할 수 있습니다.</p>
          </div>
          <div className="App-content">
            <h2>더 많은 기능을 추가할 예정입니다.</h2>
            <p>미리 초대해두고 업데이트 될 기능을 발빠르게 만나보세요!</p>
          </div>
        </div>
      </div>
      <footer className="App-footer">
        <div>
          <Link href="/policy/tos">이용약관</Link> | <Link href="/policy/privacy">개인정보 처리방침</Link>
        </div>
        <code>© {new Date().getFullYear()} aroxu. All rights reserved.</code>
      </footer>
    </main>
  );
}
