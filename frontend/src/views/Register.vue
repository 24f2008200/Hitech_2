<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary w-100" type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const router = useRouter();

async function login() {
  // ⚡ Hook this to your Flask backend later
  console.log("Logging in:", email.value);

  // Fake login → admin if email contains "admin"
  if (email.value.includes("admin")) {
    localStorage.setItem("is_admin", "true");
    router.push("/admin");
  } else {
    localStorage.setItem("is_admin", "false");
    router.push("/user");
  }
}
</script>
