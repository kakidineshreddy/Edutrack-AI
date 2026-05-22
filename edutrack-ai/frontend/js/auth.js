/* Authentication Management Framework */

// Retrieves the token stored in localStorage
const getStoredToken = () => {
  return localStorage.getItem('edutrack_token');
};

// Checks if a token exists locally
const isLoggedIn = () => {
  const token = getStoredToken();
  return !!token;
};

// Log in the user by verifying credentials against backend API
const loginUser = async (email, password) => {
  try {
    const data = await login(email, password);
    if (data && data.access_token) {
      localStorage.setItem('edutrack_token', data.access_token);
      
      // Fetch user profile info and store it
      const profile = await getMe();
      if (profile) {
        localStorage.setItem('edutrack_user_email', profile.email);
        localStorage.setItem('edutrack_user_role', profile.role);
      }
      
      window.location.href = 'dashboard.html';
      return true;
    }
    return false;
  } catch (error) {
    console.error('Authentication attempt failed:', error);
    throw error;
  }
};

// Clears credentials and redirects to login portal
const logoutUser = () => {
  localStorage.removeItem('edutrack_token');
  localStorage.removeItem('edutrack_user_email');
  localStorage.removeItem('edutrack_user_role');
  window.location.href = 'login.html';
};

// Checks page-level access permissions
const checkAuth = () => {
  if (!isLoggedIn()) {
    console.warn("Access denied. Token missing. Redirecting to login.");
    window.location.href = 'login.html';
  }
};

// Initialize dashboard header profile elements
const initUserProfileHeader = () => {
  const email = localStorage.getItem('edutrack_user_email') || 'User';
  const role = localStorage.getItem('edutrack_user_role') || 'staff';
  
  const welcomeText = document.getElementById('user-welcome-text');
  const roleText = document.getElementById('user-role-text');
  const avatar = document.getElementById('user-profile-avatar');
  
  if (welcomeText) {
    const namePrefix = email.split('@')[0];
    const capitalizedName = namePrefix.charAt(0).toUpperCase() + namePrefix.slice(1);
    welcomeText.textContent = `Welcome, ${capitalizedName}`;
  }
  
  if (roleText) {
    roleText.textContent = role.toUpperCase();
  }
  
  if (avatar) {
    avatar.textContent = email.charAt(0).toUpperCase();
  }
};
