<template>
  <div class="container mt-4">
    <h2>Registered Users</h2>

    <DataTable :columns="userCols" :rows="users">
      <!-- Custom cell for From -->
      <template #start_time="{ row }">
        {{ f_date(row.start_time) }}
      </template>
      <!-- Custom cell for To -->
      <template #end_time="{ row }">
        {{ f_date(row.end_time) }}
      </template>
      <!-- Custom cell for Action -->
      <template #status="{ row }">
        <button v-if="row.status === 'active'" class="btn btn-sm btn-danger" @click="releaseSpot(row.id)">
          Release
        </button>
        <span v-else class="badge bg-success">Parked Out</span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuth } from "../stores/auth";
import { apiFetch } from "@/api";
import DataTable from "@/components/DataTable.vue";

const { token } = useAuth();
const users = ref([]);
const userCols = [
  { key: "id", label: "ID" },
  { key: "name", label: "Name" },
  { key: "email", label: "E-Mail" },
  { key: "mobile", label: "Mobile" },
  { key: "address", label: "Address" },
  { key: "status", label: "Action" }
];

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
