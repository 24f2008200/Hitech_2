<template>
  <div class="container mt-4">
    <h2>Parking Lots</h2>

    <div class="row">
      <ParkingLotCard v-for="lot in lots" :key="lot.id" :lot="lot" />
    </div>

    <!-- Add Lot Button -->
    <div class="text-center mt-4">
      <button
        class="btn btn-primary btn-lg"
        data-bs-toggle="modal"
        data-bs-target="#addLotModal"
      >
        + Add Lot
      </button>
    </div>

    <!-- Add Lot Modal -->
    <div
      class="modal fade"
      id="addLotModal"
      tabindex="-1"
      aria-labelledby="addLotModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addLotModalLabel">Add New Lot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addLot">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="newLot.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <input v-model="newLot.address" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Pin Code</label>
                <input v-model="newLot.pin_code" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Price (₹)</label>
                <input v-model.number="newLot.price" type="number" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Number of Spots</label>
                <input v-model.number="newLot.number_of_spots" type="number" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-success">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ParkingLotCard from "../components/ParkingLotCard.vue"
import { apiFetch } from "@/api";

export default {
  components: { ParkingLotCard },
  data() {
    return {
      lots: [],
      newLot: { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
    }
  },
  async mounted() {
    await this.fetchLots()
  },
  methods: {
    async fetchLots() {
      const token = localStorage.getItem("access_token")
      try {
        const res = await apiFetch("/admin/lots", {
          headers: { "Authorization": `Bearer ${token}` }
        })
        this.lots = await res.json()
      } catch (err) {
        console.error("Error fetching lots:", err)
      }
    },
    async addLot() {
      const token = localStorage.getItem("access_token")
      try {
        const res = await apiFetch("/admin/lots", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(this.newLot)
        })

        if (res.ok) {
          // Close modal
          const modal = bootstrap.Modal.getInstance(document.getElementById("addLotModal"))
          modal.hide()

          // Refresh lots
          await this.fetchLots()

          // Reset form
          this.newLot = { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
        } else {
          console.error("Failed to add lot")
        }
      } catch (err) {
        console.error("Error adding lot:", err)
      }
    }
  }
}
</script>
