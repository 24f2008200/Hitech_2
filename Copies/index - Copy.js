import { createRouter, createWebHistory } from "vue-router";
import AdminDashboard from "../views/AdminDashboard.vue";
import UserDashboard from "../views/UserDashboard.vue";
import Login from "../views/Login.vue";
import Users from "../views/Users.vue";
import Search from "../views/Search.vue";
import Summary from "../views/Summary.vue";
import Profile from "../views/Profile.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/admin", component: AdminDashboard },
  { path: "/user", component: UserDashboard },
  { path: "/users", component: Users },
  { path: "/search", component: Search },
  { path: "/summary", component: Summary },
  { path: "/profile", component: Profile }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
