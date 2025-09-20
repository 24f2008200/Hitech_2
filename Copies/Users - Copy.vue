<template>
  <div class="container mt-4">
    <h2>Registered Users</h2>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Mobile</th>
          <th>Address</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.mobile }}</td>
          <td>{{ u.address }}</td>
          <td>
            <span :class="u.blocked ? 'text-danger' : 'text-success'">
              {{ u.blocked ? 'Blocked' : 'Active' }}
            </span>
          </td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="editUser(u)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="toggleBlock(u)">
              {{ u.blocked ? 'Unblock' : 'Block' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuth } from "../stores/auth";
import { apiFetch } from "@/api";

const { token } = useAuth();
const users = ref([]);

async function fetchUsers() {
  const res = await apiFetch("/admin/users", {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    users.value = await res.json();
  }
}

function editUser(user) {
  alert(`TODO: Open edit form for ${user.email}`);
}

async function toggleBlock(user) {
  const res = await apiFetch(`/admin/users/${user.id}/block`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    user.blocked = !user.blocked;
  }
}

onMounted(fetchUsers);
</script>
