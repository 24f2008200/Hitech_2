<template>
  <div class="container mt-4">
    <h2>Parking Lots</h2>

    <div class="row">
      <div class="col-md-4 mb-4" v-for="lot in lots" :key="lot.id">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ lot.name }} <small class="text-muted">({{ lot.address }})</small></h5>
            <p class="text-success fw-bold">
              Occupied: {{ lot.occupied_spots }}/{{ lot.number_of_spots }}
            </p>
            <div class="mb-2">
              <a href="#" class="text-warning me-2" @click="openEditModal(lot)">Edit</a> |
              <a href="#" class="text-danger ms-2" @click="deleteLot(lot.id)">Delete</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Lot Button -->
    <div class="text-center mt-4">
      <button class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#lotModal">
        + Add Lot
      </button>
    </div>

    <!-- Add/Edit Lot Modal -->
    <div class="modal fade" id="lotModal" tabindex="-1" aria-labelledby="lotModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="lotModalLabel">{{ editingLot ? "Edit Lot" : "Add Lot" }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveLot">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="formLot.name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Address</label>
                <input v-model="formLot.address" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Pin Code</label>
                <input v-model="formLot.pin_code" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Price (₹)</label>
                <input v-model.number="formLot.price" type="number" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Number of Spots</label>
                <input v-model.number="formLot.number_of_spots" type="number" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-success">{{ editingLot ? "Update" : "Save" }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lots: [],
      editingLot: null, // when set, modal is for editing
      formLot: { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
    }
  },
  async mounted() {
    await this.fetchLots()
  },
  methods: {
    async fetchLots() {
      const token = localStorage.getItem("access_token")
      const res = await fetch("http://localhost:5000/admin/lots", {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.lots = await res.json()
    },
    openEditModal(lot) {
      this.editingLot = lot.id
      this.formLot = { ...lot } // clone
      const modal = new bootstrap.Modal(document.getElementById("lotModal"))
      modal.show()
    },
    async saveLot() {
      const token = localStorage.getItem("access_token")
      const url = this.editingLot
        ? `http://localhost:5000/admin/lots/${this.editingLot}`
        : "http://localhost:5000/admin/lots"
      const method = this.editingLot ? "PUT" : "POST"

      await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(this.formLot)
      })

      // Refresh
      await this.fetchLots()

      // Reset state
      this.formLot = { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
      this.editingLot = null
      bootstrap.Modal.getInstance(document.getElementById("lotModal")).hide()
    },
    async deleteLot(lotId) {
      if (!confirm("Are you sure you want to delete this lot?")) return

      const token = localStorage.getItem("access_token")
      await fetch(`http://localhost:5000/admin/lots/${lotId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` }
      })

      await this.fetchLots()
    }
  }
}
</script>
