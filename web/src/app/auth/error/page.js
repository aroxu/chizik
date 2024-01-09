import { useSession } from "next-auth/react";
import "../../manage/manage.scss";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRefresh, faWarning } from "@fortawesome/free-solid-svg-icons";
import Link from "next/link";

const AuthError = () => {
  const { status } = useSession();
  const router = useRouter();

  return (
    <div className="ManageAuth">
      {status === "loading" ? (
        <>
          <FontAwesomeIcon className="LoadingIcon" icon={faRefresh} size="6x" />
          <br />
          <h4>로드 중...</h4>
          <p>잠시만 기다려 주세요</p>
        </>
      ) : (
        <>
          <FontAwesomeIcon icon={faWarning} size="6x" />
          <br />
          <h4>인증 도중 오류가 발생하였습니다.</h4>
          <p>사용자가 인증을 취소하거나 Discord에서 인증 오류가 발생하였습니다.</p>
          <br />
          <Link role="button" className="outline" href="/">
            <span>메인페이지로 돌아가기</span>
          </Link>
        </>
      )}
    </div>
  );
};

export default AuthError;