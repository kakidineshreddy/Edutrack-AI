const BASE_URL = 'http://127.0.0.1:8000';

// Ejects user when JWT expires
const logout = () => {
  localStorage.removeItem('edutrack_token');
  window.location.href = 'login.html';
};

// Retrieve saved token
const getToken = () => {
  return localStorage.getItem('edutrack_token');
};

// Build request headers with token injection
const authHeaders = () => {
  const token = getToken();
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

// Standardized fetch request wrapper containing 401 traps and error parsing
const makeRequest = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...authHeaders(),
        ...options.headers
      }
    });

    if (response.status === 401) {
      console.warn("Unauthorized API call. Purging token and redirecting.");
      logout();
      return null;
    }

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      const errMsg = errData.detail || `HTTP Error ${response.status}: ${response.statusText}`;
      throw new Error(errMsg);
    }

    return await response.json();
  } catch (error) {
    console.error(`API Call failed on ${url}:`, error);
    throw error;
  }
};

// Core Authentication Operations
const login = async (email, password) => {
  try {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || 'Invalid email or password');
    }

    return await response.json();
  } catch (error) {
    console.error('Login action failed:', error);
    throw error;
  }
};

const register = async (email, password, role = 'student') => {
  return makeRequest(`${BASE_URL}/auth/register`, {
    method: 'POST',
    body: JSON.stringify({ email, password, role })
  });
};

const getMe = async () => {
  return makeRequest(`${BASE_URL}/auth/me`);
};

// Student CRUD
const getStudents = async () => {
  return makeRequest(`${BASE_URL}/api/students`);
};

const getStudent = async (id) => {
  return makeRequest(`${BASE_URL}/api/students/${id}`);
};

const createStudent = async (data) => {
  return makeRequest(`${BASE_URL}/api/students`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

const updateStudent = async (id, data) => {
  return makeRequest(`${BASE_URL}/api/students/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

const deleteStudent = async (id) => {
  return makeRequest(`${BASE_URL}/api/students/${id}`, {
    method: 'DELETE'
  });
};

// Teacher CRUD
const getTeachers = async () => {
  return makeRequest(`${BASE_URL}/api/teachers`);
};

const getTeacher = async (id) => {
  return makeRequest(`${BASE_URL}/api/teachers/${id}`);
};

const createTeacher = async (data) => {
  return makeRequest(`${BASE_URL}/api/teachers`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

const updateTeacher = async (id, data) => {
  return makeRequest(`${BASE_URL}/api/teachers/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

const deleteTeacher = async (id) => {
  return makeRequest(`${BASE_URL}/api/teachers/${id}`, {
    method: 'DELETE'
  });
};

// Course CRUD
const getCourses = async () => {
  return makeRequest(`${BASE_URL}/api/courses`);
};

const getCourse = async (id) => {
  return makeRequest(`${BASE_URL}/api/courses/${id}`);
};

const createCourse = async (data) => {
  return makeRequest(`${BASE_URL}/api/courses`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

const updateCourse = async (id, data) => {
  return makeRequest(`${BASE_URL}/api/courses/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

const deleteCourse = async (id) => {
  return makeRequest(`${BASE_URL}/api/courses/${id}`, {
    method: 'DELETE'
  });
};

// Grade CRUD
const getGrades = async () => {
  return makeRequest(`${BASE_URL}/api/grades`);
};

const getGrade = async (id) => {
  return makeRequest(`${BASE_URL}/api/grades/${id}`);
};

const getStudentGrades = async (studentId) => {
  return makeRequest(`${BASE_URL}/api/grades/student/${studentId}`);
};

const createGrade = async (data) => {
  return makeRequest(`${BASE_URL}/api/grades`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

const updateGrade = async (id, data) => {
  return makeRequest(`${BASE_URL}/api/grades/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

const deleteGrade = async (id) => {
  return makeRequest(`${BASE_URL}/api/grades/${id}`, {
    method: 'DELETE'
  });
};

// Attendance CRUD
const getAttendance = async () => {
  return makeRequest(`${BASE_URL}/api/attendance`);
};

const getStudentAttendance = async (studentId) => {
  return makeRequest(`${BASE_URL}/api/attendance/student/${studentId}`);
};

const createAttendance = async (data) => {
  return makeRequest(`${BASE_URL}/api/attendance`, {
    method: 'POST',
    body: JSON.stringify(data)
  });
};

const updateAttendance = async (id, data) => {
  return makeRequest(`${BASE_URL}/api/attendance/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data)
  });
};

const deleteAttendance = async (id) => {
  return makeRequest(`${BASE_URL}/api/attendance/${id}`, {
    method: 'DELETE'
  });
};

// AI Analytics & Predictions
const getAnalytics = async () => {
  return makeRequest(`${BASE_URL}/api/analytics/performance`);
};

const getPrediction = async (studentId) => {
  return makeRequest(`${BASE_URL}/api/analytics/predictions/${studentId}`);
};

const getRecommendations = async (studentId) => {
  return makeRequest(`${BASE_URL}/api/analytics/recommendations/${studentId}`);
};
