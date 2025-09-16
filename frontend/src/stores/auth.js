// src/stores/auth.js
import { ref, computed } from "vue";

const token = ref(localStorage.getItem("access_token"));
const isAdmin = ref(localStorage.getItem("is_admin") === "true");

export function useAuth() {
  const isLoggedIn = computed(() => token.value !== null);

  function login(data) {
    // data should come from Flask: { access_token, user: { is_admin: true/false } }
    token.value = data.access_token;
    isAdmin.value = data.user.is_admin;

    // persist to localStorage
    localStorage.setItem("access_token", token.value);
    localStorage.setItem("is_admin", isAdmin.value);
  }

  function logout() {
    token.value = null;
    isAdmin.value = false;

    // clear from localStorage
    localStorage.removeItem("access_token");
    localStorage.removeItem("is_admin");
  }

  return { token, isAdmin, isLoggedIn, login, logout };
}
