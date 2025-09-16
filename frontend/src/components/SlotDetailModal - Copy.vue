<template>
  <div class="modal fade show" tabindex="-1" role="dialog" style="display: block; background: rgba(0,0,0,0.5);"
    v-if="visible">
    <div class="modal-dialog" role="document">
      <div class="modal-content">

        <div class="modal-header">
          <h5 class="modal-title">{{ deletable  ? 'Occupied Details' : 'Available/ Delete' }}</h5>
          <button type="button" class="btn-close" @click="doClose"></button>
        </div>

        <div class="modal-body">
          <p><strong>ID:</strong> {{ slot.id }}</p>
          <p>
            <strong>Status:</strong>
            <span :class="slot.status == 'O' ? 'text-danger' : 'text-success'">
              {{ deletable  ? 'Occupied' : 'Available' }}
            </span>
          </p>
          <p><strong>Lot ID:</strong> {{ slot.lot_id }}</p>
          <p><strong>Label:</strong> {{ slot.label }}</p>
          <p><strong>Vehicle Number:</strong> {{ reservation.vehicle_number }}</p>
          <p><strong>Start Time:</strong> {{ reservation.start_time }}</p>
        </div>

        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-success" v-if="deletable" @click="doDelete">Delete</button>
          <button type="button" class="btn btn-secondary me-2" @click="doClose">Cancel</button>
        </div>
        <!-- <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="clickSClose">Close</button>
        </div> -->

      </div>
    </div>
  </div>
</template>

<!-- <script>
export default {
  name: 'SlotDetailModal',
  props: {
    visible: { type: Boolean, default: false },
    slot: { type: Object, default: () => ({}) },
    reservation: { type: Object, default: () => ({}) }
  }

  }

</script> -->
<script setup>
import { defineProps, defineEmits } from "vue";

// Props
const props = defineProps({
  slot: {
    type: Object,
    default: () => ({}),
    required: true
  },
  reservation: {
    type: Object,
    default: () => ({}),
    required: false
  },
  deletable: {
    type: Boolean,
    default: () => (slot.status == 'O')
  } 
});

const emit = defineEmits(["close", "delete"]);
function doClose() {
  emit("close");
}

function doDelete() {
  if (!confirm("Are you sure you want to delete this lot?")) return
  emit("delete", props.slot.id);
}
</script>

<style scoped></style>