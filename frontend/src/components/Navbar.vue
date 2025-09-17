<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <span class="navbar-brand">
      {{ welcomeText }}
    </span>

    <ul class="navbar-nav me-auto">
      <!-- Public Navbar -->
      <template v-if="!isLoggedIn">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/login">Login</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/register">Register</RouterLink>
        </li>
      </template>

      <!-- Show admin-only links -->
      <template v-else-if="isAdmin">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/admin">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/users">Users</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/search">Search</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/admin/summary">Summary</RouterLink>
        </li>
      </template>
      <!-- User Navbar -->
      <template v-else>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/user">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/user/summary">Summary</RouterLink>
        </li>
      </template>

    </ul>
    <!-- Shared links -->
    <ul class="navbar-nav">
      <li class="nav-item">
        <RouterLink class="nav-link" to="/profile">Edit Profile</RouterLink>
      </li>
      <li class="nav-item">
        <button class="btn btn-sm btn-outline-light ms-2" @click="doLogout">
          Logout
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth";
import { apiFetch } from "@/api";
const { isLoggedIn, isAdmin, logout } = useAuth();


const router = useRouter();
// const isLoggedIn = computed(() =>
//   localStorage.getItem("access_token") !== null);

// const isAdmin = localStorage.getItem("is_admin") === "true";
const welcomeText = computed(() => {
  if (!isLoggedIn.value) {
    return "Welcome, Guest"
  }
  return isAdmin.value ? "Welcome to Admin" : "Welcome to User"
})
console.log("Navbar - msg:", welcomeText.value);
console.log("Navbar - isLoggedIn:", isLoggedIn.value);
console.log("Navbar - isAdmin:", isAdmin.value);


async function doLogout() {
  try {
    await apiFetch("/auth/logout", {
      method: "POST",
      credentials: "include",
    });
  } catch (e) {
    console.warn("Logout request failed:", e);
  }
  localStorage.removeItem("access_token");
  localStorage.removeItem("is_admin");
  logout();
  router.push("/");
}
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
  color: #ff4444;
  /* red accent for "Welcome" */
}

.nav-link {
  color: #fff !important;
}

.nav-link.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>
