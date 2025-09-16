<template>
  <div class="container mt-4">
    <h2>Search</h2>

    <input v-model="query" class="form-control mb-3" placeholder="Search by name, email, or phone" />

    <button class="btn btn-primary mb-3" @click="doSearch">Search</button>

    <div v-if="results.length">
      <h5>Results:</h5>
      <ul class="list-group">
        <li class="list-group-item" v-for="r in results" :key="r.id">
          {{ r.email }} — {{ r.phone }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuth } from "../stores/auth";

const { token } = useAuth();
const query = ref("");
const results = ref([]);

async function doSearch() {
  if (!query.value) return;

  const res = await fetch(`http://localhost:5000/admin/search?query=${query.value}`, {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    results.value = await res.json();
  }
}
</script>
