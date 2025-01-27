import { useAuth } from "./AuthContext";
import LockedPage from "./LockedPage";

const ProtectedRoute = ({ page }) => {
  const { loggedIn } = useAuth();

  return loggedIn ? page : <LockedPage />;
};

export default ProtectedRoute;
