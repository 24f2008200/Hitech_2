<template>
  <div class="container mt-4">
    <h2>Summary Reports</h2>

    <div class="row text-center mb-4">
      <div class="col">
        <h5>Total Users</h5>
        <p>{{ summary.total_users }}</p>
      </div>
      <div class="col">
        <h5>Active Reservations</h5>
        <p>{{ summary.active_reservations }}</p>
      </div>
      <div class="col">
        <h5>Parking Lots</h5>
        <p>{{ summary.lots }}</p>
      </div>
    </div>

    <h4>Revenue Chart</h4>
    <LineChart v-if="summary.revenue" :data="summary.revenue" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuth } from "../stores/auth";
import LineChart from "../components/LineChart.vue";
import { apiFetch } from "@/api";

const { token } = useAuth();
const summary = ref({});

async function fetchSummary() {
  const res = await apiFetch("/admin/summary", {
    headers: { Authorization: `Bearer ${token.value}` }
  });
  if (res.ok) {
    summary.value = await res.json();
  }
}

onMounted(fetchSummary);
</script>
