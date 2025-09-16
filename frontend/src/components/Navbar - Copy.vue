
<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light px-3">
    <span class="navbar-text fw-bold text-success">Vehicle Parking App</span>
    <div class="mx-auto">
      <router-link to="/" class="mx-2">Login</router-link>
      <router-link to="/admin" class="mx-2">Admin</router-link>
      <router-link to="/user" class="mx-2">User</router-link>
    </div>
    <button v-if="isLoggedIn" @click="logout" class="btn btn-sm btn-outline-danger">
      Logout
    </button>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isLoggedIn = ref(true); // ⚡ later: make this dynamic

async function logout() {
  await fetch("http://localhost:5000/auth/logout", {
    method: "POST",
    credentials: "include",
  });
  localStorage.removeItem("access_token");
  localStorage.removeItem("is_admin");
  isLoggedIn.value = false;
  router.push("/");
}
</script>

<style scoped>
.navbar-brand { font-weight: bold; }
</style>