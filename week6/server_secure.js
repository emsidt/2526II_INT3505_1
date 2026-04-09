const express = require("express");
const jwt = require("jsonwebtoken");
const cookieParser = require("cookie-parser");

const app = express();
app.use(express.json());
app.use(cookieParser());

const PORT = 3000;
const ACCESS_SECRET = "demo_access_secret_123";
const REFRESH_SECRET = "demo_refresh_secret_456";

const users = [
  { id: 1, username: "admin", password: "123", role: "admin" },
  { id: 2, username: "user", password: "123", role: "user" }
];

let refreshTokens = [];
function createAccessToken(user) {
  return jwt.sign(
    { id: user.id, username: user.username, role: user.role },
    ACCESS_SECRET,
    { expiresIn: "15m" }
  );
}

function createRefreshToken(user) {
  return jwt.sign(
    { id: user.id, username: user.username },
    REFRESH_SECRET,
    { expiresIn: "7d" }
  );
}

function authenticateToken(req, res, next) {
  const token = req.cookies.accessToken;

  if (!token) {
    return res.status(401).json({ message: "Không có access token" });
  }

  try {
    const user = jwt.verify(token, ACCESS_SECRET);
    req.user = user;
    next();
  } catch (err) {
    return res.status(403).json({ message: "Token không hợp lệ hoặc hết hạn" });
  }
}

function authorizeRole(role) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ message: "Không đủ quyền" });
    }
    next();
  };
}

// Login
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  const user = users.find(
    (u) => u.username === username && u.password === password
  );

  if (!user) {
    return res.status(401).json({ message: "Sai tài khoản hoặc mật khẩu" });
  }

  const accessToken = createAccessToken(user);
  const refreshToken = createRefreshToken(user);

  refreshTokens.push(refreshToken);

  res.cookie("accessToken", accessToken, {
    httpOnly: true,
    sameSite: "lax"
  });

  res.cookie("refreshToken", refreshToken, {
    httpOnly: true,
    sameSite: "lax"
  });

  res.json({ message: "Đăng nhập thành công", role: user.role });
});

// Refresh
app.post("/refresh", (req, res) => {
  const refreshToken = req.cookies.refreshToken;

  if (!refreshToken) {
    return res.status(401).json({ message: "Không có refresh token" });
  }

  if (!refreshTokens.includes(refreshToken)) {
    return res.status(403).json({ message: "Refresh token không hợp lệ" });
  }

  try {
    const user = jwt.verify(refreshToken, REFRESH_SECRET);
    const accessToken = createAccessToken(user);

    res.cookie("accessToken", accessToken, {
      httpOnly: true,
      sameSite: "lax"
    });

    res.json({ message: "Làm mới access token thành công" });
  } catch (err) {
    return res.status(403).json({ message: "Refresh token hết hạn hoặc lỗi" });
  }
});

// Profile
app.get("/profile", authenticateToken, (req, res) => {
  res.json({
    message: "Thông tin người dùng",
    user: req.user
  });
});

// Admin only
app.get("/admin", authenticateToken, authorizeRole("admin"), (req, res) => {
  res.json({ message: "Chào admin" });
});

// Logout
app.post("/logout", (req, res) => {
  const refreshToken = req.cookies.refreshToken;
  refreshTokens = refreshTokens.filter((t) => t !== refreshToken);

  res.clearCookie("accessToken");
  res.clearCookie("refreshToken");

  res.json({ message: "Đăng xuất thành công" });
});

app.listen(PORT, () => {
  console.log(`Server đang chạy tại http://localhost:${PORT}`);
});