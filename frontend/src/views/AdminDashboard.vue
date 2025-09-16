<template>
  <div class="container mt-4">
    <h2>Parking Lots</h2>

    <div class="row">
      <ParkingLotCard v-for="lot in lots" :key="lot.id" :lot="lot" @edit-lot="handleEditLot"
        @delete-lot="handleDeleteLot" @slot-click="showSlotDetails" />
    </div>
    <!-- Popup modal -->
    <SlotDetailModal :visible="isModalOpen" :slot="selectedSlot" :reservation="selectedReservation" @close="isModalOpen = false" />
    <!-- Add Lot Button -->
    <div class="text-center mt-4">
      <!-- <button class="btn btn-primary btn-lg" data-bs-toggle="modal" data-bs-target="#lotModal" @click="handleEditLot(null)">  -->
      <button class="btn btn-primary btn-lg" @click="handleEditLot(null)">
        + Add Lot
      </button>
    </div>

    <!-- Add/Edit Lot Modal -->
    <div class="modal fade" id="lotModal" tabindex="-1" aria-labelledby="lotModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="lotModalLabel">{{ isEdit ? "Edit Lot" : "Add New Lot" }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateLot">
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
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-success">{{ isEdit ? "Update" : "Save" }}</button>
                <button type="button" class="btn btn-secondary me-2" @click="closeModalAndRefresh">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ParkingLotCard from "../components/ParkingLotCard.vue"
import SlotDetailModal from '../components/SlotDetailModal.vue'
import { Modal } from "bootstrap"
import { ref } from 'vue'


const lots = ref([]) // fetched from API

const isModalOpen = ref(false)
const selectedSlot = ref({})
const selectedReservation = ref({})


export default {
  name: 'AdminDashboard',
  components: { ParkingLotCard, SlotDetailModal },
  data() {
    return {
      lots: [],
      formLot: { name: "", address: "", pin_code: "", price: null, number_of_spots: null },
      isEdit: false,
      editId: null,
      isModalOpen: false,
      selectedSlot: {},
      selectedReservation: null 
    }

  },
  async mounted() {
    await this.fetchLots()
  },


  methods: {

    async fetchLots() {
      const token = localStorage.getItem("access_token")
      try {
        const res = await fetch("http://localhost:5000/admin/lots", {
          headers: { "Authorization": `Bearer ${token}` }
        })
        this.lots = await res.json()
      } catch (err) {
        console.error("Error fetching lots:", err)
      }
    },
    showSlotDetails(slot) {
      console.log("Slot clicked:", slot)
      this.selectedSlot = slot
      this.selectedReservation = slot.current_reservation
      this.isModalOpen = true
    },
    showModal() {
      const modalEl = document.getElementById('lotModal')
      const modal = Modal.getOrCreateInstance(modalEl) // one instance
      modal.show()
    },
    openAddForm() {
      this.isEdit = false
      this.formLot = { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
      this.$nextTick(() => {
        this.showModal()
      })
    },
    handleEditLot(lot) {
      if (!lot) {
        this.isEdit = false
        this.formLot = { name: "", address: "", pin_code: "", price: null, number_of_spots: null }
      } else {
        this.isEdit = true
        this.editId = lot.id
        this.formLot = { ...lot }
      }
      this.$nextTick(() => {
        this.showModal()
      })
    },

    async updateLot() {
      const token = localStorage.getItem("access_token")
      let url, method
      if (this.isEdit) {
        url = `http://localhost:5000/admin/lots/${this.editId}`
        method = "PUT"
      } else {
        url = "http://localhost:5000/admin/lots"
        method = "POST"
      }
      console.log("Submitting to:", url, method, this.formLot)
      try {
        const res = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          },
          body: JSON.stringify(this.formLot)
        })

        if (res.ok) {
          await this.closeModalAndRefresh()
        } else {
          console.error("Failed to update lot")
        }
      } catch (err) {
        console.error("Error updating lot:", err)
      }
    },
    async handleDeleteLot(id) {
      const token = localStorage.getItem("access_token")
      if (!confirm("Are you sure you want to delete this lot?")) return
      try {
        const res = await fetch(`http://localhost:5000/admin/lots/${id}`, {
          method: "DELETE",
          headers: { "Authorization": `Bearer ${token}` }
        })
        if (res.ok) {
          await this.fetchLots()
        } else {
          console.error("Failed to delete lot")
        }
      } catch (err) {
        console.error("Error deleting lot:", err)
      }
    },
    async closeModalAndRefresh() {
      const modalEl = document.getElementById('lotModal')
      const modal = Modal.getInstance(modalEl)
      if (!modal) return

      // Wait for modal to fully hide before refreshing
      modalEl.addEventListener('hidden.bs.modal', async () => {
        await this.fetchLots() // update DOM safely
        this.formLot = { name: '', address: '', pin_code: '', price: null, number_of_spots: null }
        this.editId = null
        this.isEdit = false
      }, { once: true })

      modal.hide()
    }
  }
}
</script>
