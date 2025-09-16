<template>
  <div class="container mt-4">
    <h2 class="mb-4">User Dashboard</h2>

    <!-- Recent Parking History -->
    <div class="card mb-4">
      <div class="card-header bg-primary text-white">
        Recent Parking History
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Location</th>
              <th>Vehicle No</th>
              <th>Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reservations" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.spot_id }}</td>
              <td>{{ r.vehicle_number }}</td>
              <td>{{ r.start_time }}</td>
              <td>
                <button v-if="r.active" class="btn btn-sm btn-danger" @click="releaseSpot(r.id)">
                  Release
                </button>
                <span v-else class="badge bg-success">Parked Out</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Parking Lots by Pin Code -->
    <div class="card">
      <div class="card-header bg-success text-white">
        Search Parking Lots by Pin Code
      </div>
      <div class="card-body">
        <div class="row mb-3">
          <div class="col-md-6">
            <select v-model="selectedPin" class="form-select" @change="fetchLots">
              <option disabled value="">Select Pin Code</option>
              <option v-for="pin in pinCodes" :key="pin" :value="pin">
                {{ pin }}
              </option>
            </select>
          </div>
        </div>
        <!-- Booking Modal -->
        <div class="modal fade" id="bookingModal" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Book Parking Slot</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="confirmBooking">
                  <div class="mb-3">
                    <label class="form-label">Vehicle Number</label>
                    <input v-model="form.vehicle_no" type="text" class="form-control" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">User Name</label>
                    <input v-model="form.user_name" type="text" class="form-control" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">User ID</label>
                    <input v-model="form.user_id" type="text" class="form-control" required />
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button class="btn btn-primary" @click="confirmBooking">Confirm Booking</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="lots.length">
          <h5>Parking Lots @ {{ selectedPin }}</h5>
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Address</th>
                <th>Availability</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in lots" :key="lot.id">
                <td>{{ lot.id }}</td>
                <td>{{ lot.address }}</td>
                <td>{{ lot.available_spots }}</td>
                <td>
                  <button class="btn btn-sm btn-primary" :disabled="lot.available_spots === 0"
                    @click="openBookingModal(lot)">
                    Book
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="text-muted">No lots available for this pin code.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuth } from "../stores/auth";
import * as bootstrap from "bootstrap";

const { token } = useAuth();

// State
const reservations = ref([]);
const pinCodes = ref([]);
const selectedPin = ref("");
const lots = ref([]);

// state for modal + form
const selectedLot = ref(null);
const bookingModal = ref(null);
const form = ref({
  vehicle_no: "",
  user_name: "",
  user_id: ""
});
// Open modal
function openBookingModal(lot) {
  selectedLot.value = lot;
  form.value = { vehicle_no: "", user_name: "", user_id: "" };

  const modalEl = document.getElementById("bookingModal");
  bookingModal.value = new bootstrap.Modal(modalEl);
  bookingModal.value.show();
}

// Confirm booking
async function confirmBooking() {
  if (!selectedLot.value) return;

  const res = await fetch("http://localhost:5000/user/book", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token.value}`
    },
    body: JSON.stringify({
      lot_id: selectedLot.value.id,
      vehicle_no: form.value.vehicle_no,
      user_name: form.value.user_name,
      user_id: form.value.user_id
    })
  });

  if (res.ok) {
    alert("Slot booked successfully!");
    bookingModal.value.hide();
    fetchLots(); // refresh list of lots
  } else {
    alert("Failed to book slot");
  }
}
// Fetch recent reservations
async function fetchReservations() {
  const res = await fetch("http://localhost:5000/user/reservations", {
    headers: { Authorization: `Bearer ${token.value}` },
  });
  if (res.ok) {
    reservations.value = await res.json();
  }
}

// Release a spot
async function releaseSpot(reservationId) {
  const res = await fetch(
    `http://localhost:5000/user/reservations/${reservationId}/release`,
    {
      method: "PATCH",
      headers: { Authorization: `Bearer ${token.value}` },
    }
  );
  if (res.ok) {
    reservations.value = reservations.value.map((r) =>
      r.id === reservationId ? { ...r, active: false } : r
    );
  }
}

// Fetch pin codes
async function fetchPinCodes() {
  const res = await fetch("http://localhost:5000/user/pincodes", {
    headers: { Authorization: `Bearer ${token.value}` },
  });
  if (res.ok) {
    pinCodes.value = await res.json();
  }
}

// Fetch lots by pin code
async function fetchLots() {
  if (!selectedPin.value) return;
  const res = await fetch(
    `http://localhost:5000/user/lots?pin_code=${selectedPin.value}`,
    {
      headers: { Authorization: `Bearer ${token.value}` },
    }
  );
  if (res.ok) {
    lots.value = await res.json();
  }
}

// Book a spot
async function bookSpot(lotId) {
  const res = await fetch(`http://localhost:5000/user/reservations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token.value}`,
    },
    body: JSON.stringify({ lot_id: lotId }),
  });
  if (res.ok) {
    fetchReservations(); // refresh reservations
    fetchLots(); // refresh availability
  }
}

onMounted(() => {
  fetchReservations();
  fetchPinCodes();
});
</script>
