import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import UserDashboard from "../views/UserDashboard.vue";
import Users from "../views/Users.vue";
import Search from "../views/Search.vue";
import Summary from "../views/Summary.vue";
import Profile from "../views/Profile.vue";



const routes = [
  // Public (general) routes
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", name: "Register", component: Register },

  // User routes
  { path: "/user", component: UserDashboard, meta: { requiresAuth: true, role: "user" } },
  { path: "/user/summary", component: Summary, meta: { requiresAuth: true, role: "user" } },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },

  // Admin routes
  { path: "/admin", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" } },
  { path: "/users", component: Users, meta: { requiresAuth: true, role: "admin" } },
  { path: "/admin/summary", component: Summary, meta: { requiresAuth: true } },
  { path: "/search", component: Search, meta: { requiresAuth: true, role: "admin" } }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  const isAdmin = localStorage.getItem("is_admin") === "true";

  if (to.meta.requiresAuth && !token) {
    // Not logged in → send to login
    return next("/login");
  }

  if (to.meta.role === "admin" && !isAdmin) {
    // Logged in but not admin
    return next("/user");
  }

  if (to.meta.role === "user" && isAdmin) {
    // Admin trying to access user-only route
    return next("/admin");
  }

  next();
});

export default router;
