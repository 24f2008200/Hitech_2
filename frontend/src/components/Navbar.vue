<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <span class="navbar-brand">
      {{ welcomeText }}
    </span>

    <!-- Public Navbar -->
    <template v-if="!isLoggedIn">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/login">Login</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/register">Register</RouterLink>
        </li>
      </ul>
    </template>

    <!-- Show admin-only links -->
    <template v-else-if="isAdmin">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/admin">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/users">Users</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/admin/summary">Summary</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/search">Search</RouterLink>
        </li>
      </ul>
      <!--  Radio buttons for search type -->
      <form class="d-flex align-items-center text-white me-3">
        <!-- <span class="search-label" @click="onSearchByClick">
          Search By
        </span> -->
        <!-- <label class="me-2">Search by:</label> -->
        <div class="form-check form-check-inline text-white">
          <input v-model="searchStore.searchValue" />
        </div>
        <div class="form-check form-check-inline text-white">
          <input class="form-check-input" type="radio" id="searchUser" value="user" v-model="searchStore.searchType" />
          <label class="form-check-label" for="searchUser">User</label>
        </div>
        <div class="form-check form-check-inline text-white">
          <input class="form-check-input" type="radio" id="searchReservation" value="reservation"
            v-model="searchStore.searchType" />
          <label class="form-check-label" for="searchReservation">Reservation</label>
        </div>
        <div class="form-check form-check-inline text-white">
          <input class="form-check-input" type="radio" id="searchLot" value="lot" v-model="searchStore.searchType" />
          <label class="form-check-label" for="searchLot">Lot</label>
        </div>
      </form>


    </template>
    <!-- User Navbar -->
    <template v-else>
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <RouterLink class="nav-link" to="/user">Home</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/user/summary">Summary</RouterLink>
        </li>

      </ul>
    </template>

    <!-- Shared links -->
    <ul class="navbar-nav">
      <li class="nav-item">
        <!-- <RouterLink class="nav-link" to="/profile">Edit Profile</RouterLink> -->
        <button class="btn btn-outline-primary btn-sm" @click="openProfile">Profile</button>
      </li>
      <li class="nav-item">
        <button class="btn btn-sm btn-outline-light ms-2" @click="doLogout">
          Logout
        </button>
      </li>
    </ul>
  </nav>
  <div >
    <UserProfileModal :userId="userId" :currentUserIsAdmin="currentUserIsAdmin" :show="show" @closed="show = false">
    </UserProfileModal>
  </div>

</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../stores/auth";
import { useSearchStore } from "../stores/search";
import { apiFetch } from "@/api";
import { watch } from "vue";
import UserProfileModal from '../components/UserProfileModal.vue';


const { isLoggedIn, isAdmin, logout } = useAuth();

const userId = ref();
const show = ref(false);
let currentUserIsAdmin = ref(false);

const searchStore = useSearchStore();
// const searchType = searchStore.searchType;
const router = useRouter();

const welcomeText = computed(() => {
  if (!isLoggedIn.value) {
    return "Welcome, Guest"
  }
  return isAdmin.value ? "Welcome to Admin" : "Welcome to User"
})

watch(
  () => searchStore.searchType,
  (newVal) => {
    router.push("/search"); // navigate once type changes
    searchStore.triggerNavbarAction();
  }
);
function openProfile() {
  const { isAdmin, userName, userId: uid } = useAuth()
  userId.value = parseInt(uid.value)
  currentUserIsAdmin.value = isAdmin.value
  show.value = true

}
function onSearchByClick() {
  searchStore.triggerNavbarAction();
}
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
