import { signOut } from "next-auth/react";
import "./manage.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSignOut } from "@fortawesome/free-solid-svg-icons";

const Dashboard = ({ session }) => {
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
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
        <div className="MainContent">
          <h1>관리</h1>
          <p>아직 준비중인 페이지입니다.</p>
        </div>
      </main>
    </>
  );
};

export default Dashboard;
