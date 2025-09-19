<template>
  <div class="container mt-4">
    <h2>Admin Search</h2>
    <div v-if="searchType === 'user' " class="row text-center mb-4">
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
          <button v-if="row.status === 'active'" class="btn btn-sm btn-danger" @click="showDetails(row.id)">
            Release
          </button>
          <span v-else class="badge bg-success">Parked Out</span>
        </template>
      </DataTable>

    </div>


  </div>
</template>

<script setup>
import { ref } from "vue";
import { apiFetch } from "../api";
import { useSearchStore } from "../stores/search";
import DataTable from "@/components/DataTable.vue";

const userCols = [
  { key: "lot_prefix", label: "ID" ,filterType :"select"},
  { key: "spot_id", label: "Location" },
  { key: "vehicle_number", label: "Vehicle No" },
  { key: "start_time", label: "From" },
  { key: "end_time", label: "To" },
  { key: "driver_name", label: "Driver Name" },
  { key: "driver_contact", label: "Driver Contact" },
  { key: "status", label: "Action" }
];

const searchBy = ref("");
const searchValue = ref("");
const results = ref([]);
const searched = ref(false);
const tableHeaders = ref([]);
const users = ref([]);


const searchStore = useSearchStore();
const searchType = searchStore.searchType; // reactive



async function performSearch() {
  if (!searchBy.value || !searchValue.value) {
    alert("Please select search by and enter a value.");
    return;
  }

  try {
    // Decide endpoint based on global searchType
    const endpoint =
      searchType === "user"
        ? "/admin/search/users"
        : searchType === "reservation"
          ? "/admin/search/bookings"
          : "/admin/search/lots";

    const url = `${endpoint}?search_by=${searchBy.value}&value=${encodeURIComponent(
      searchValue.value
    )}`;

    const response = await apiFetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    results.value = data;
    searched.value = true;

    if (results.value.length > 0) {
      tableHeaders.value = Object.keys(results.value[0]);
    } else {
      tableHeaders.value = [];
    }
  } catch (error) {
    console.error("Search error:", error);
    alert("Error fetching search results.");
  }
}
// Release a spot
async function showDetails(reservationId) {
  const res = await apiFetch(`/user/release/${reservationId}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token.value}` },
  });
  if (res.ok) {
    reservations.value = reservations.value.map((r) =>
      r.id === reservationId ? { ...r, status: 'completed' } : r
    );
  }
  //fetchReservations();
}
</script>
