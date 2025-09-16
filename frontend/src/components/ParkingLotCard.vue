<template>
  <div class="col-md-4 mb-4">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="card-title">
          {{ lot.name }}
          <small class="text-muted">({{ lot.address }})</small>
        </h5>
        <p class="text-success fw-bold">
          Occupied: {{ lot.occupied_spots }}/{{ lot.number_of_spots }}
        </p>
        <div class="mb-2">
          <a href="#" class="text-warning me-2" @click.prevent="openEditModal(lot)">Edit</a> |
          <a href="#" class="text-danger ms-2" @click.prevent="deleteLot(lot.id)">Delete</a>
        </div>
        <div class="d-flex flex-wrap">
          <div v-for="slot in lot.spots" :key="slot.id" class="spot-box m-1"
            :class="slot.status =='O' ? 'occupied' : 'available'" 
            @click="clickSlot(slot)">
            {{ slot.status }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- <script>
export default {
  name: "ParkingLotCard",
  props: {
    lot: { type: Object, required: true }
  },
  emits: ["edit-lot", "delete-lot", "slot-click"],
  methods: {
    openEditModal(lot) {
      console.log("Child emitting edit-lot:", lot)
      this.$emit("edit-lot", lot);
    },
    deleteLot(id) {
      this.$emit("delete-lot", id);
    },
    clickSlot(slot) {
      this.$emit('slot-click', slot)
    }
  }
}
</script> -->

<script setup>
import { defineProps, defineEmits } from "vue";

// Props
const props = defineProps({
  lot: {
    type: Object,
    required: true
  }
});

// Emits
const emit = defineEmits(["edit-lot", "delete-lot", "slot-click"]);

// Methods
function openEditModal(lot) {
  console.log("Child emitting edit-lot:", lot);
  emit("edit-lot", lot);
}

function deleteLot(id) {
  console.log("Child emitting delete-lot:", id);
  emit("delete-lot", id);
}

function clickSlot(slot) {
  console.log("Child emitting slot-click:", slot);
  emit("slot-click", slot);
}
</script>


<style >
.spot-box {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  cursor: pointer; 
}

.available {
  background-color: #28a745;
}

.occupied {
  background-color: #dc3545;
}

.square-10 {
  width: 10px;
  height: 10px;
}
</style>
