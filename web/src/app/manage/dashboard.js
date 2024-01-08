import { signOut } from "next-auth/react";
import "./manage.scss";

const Dashboard = ({ session }) => {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome back, {session.user.name}!</p>
      <button onClick={() => signOut()}>Sign out</button>
    </div>
  );
};

export default Dashboard;
