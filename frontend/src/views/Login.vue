<template>
  <div class="container mt-5">
    <h2>Login</h2>
    <form @submit.prevent="doLogin">
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary" type="submit">Login</button>
    </form>
    <p v-if="error" class="text-danger mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth";
const { login } = useAuth();

const email = ref("");
const password = ref("");
const error = ref(null);
const router = useRouter();

async function doLogin() {
  try {
    const res = await fetch("http://localhost:5000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // send cookies/session if backend sets them
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    });

    console.log("Raw response:", res);

    // Try parsing JSON safely
    const data = await res.json().catch(() => null);
    console.log("Parsed data:", data);

    if (!res.ok) {
      error.value = data?.message || "Invalid login credentials";
      return;
    }

    login(data);
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("is_admin", data.user.is_admin);

    // Redirect based on role
    if (data.user.is_admin) {
      router.push("/admin");
    } else {
      router.push("/user");
    }
  } catch (err) {
    console.error("Login failed:", err);
    error.value = "Something went wrong.";
  }
}
</script>

