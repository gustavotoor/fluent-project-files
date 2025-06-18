
import { useAuth } from '@/contexts/AuthContext';
import { Navigate } from 'react-router-dom';

const Index = () => {
  const { user } = useAuth();
  
  // Redirect to chat if authenticated, otherwise to login
  return <Navigate to={user ? "/chat" : "/login"} replace />;
};

export default Index;
