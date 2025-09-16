<template>
  <div
    class="modal fade show"
    tabindex="-1"
    role="dialog"
    style="display: block; background: rgba(0,0,0,0.5);"
    v-if="visible"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        
        <div class="modal-header">
          <h5 class="modal-title">{{ slot.status =='O' ? 'Occupied Details' : 'Available/ Delete' }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body">
          <p><strong>ID:</strong> {{ slot.id }}</p>
          <p>
            <strong>Status:</strong>
            <span :class="slot.status =='O' ? 'text-danger' : 'text-success'">
              {{ slot.status =='O' ? 'Occupied' : 'Available' }}
            </span>
          </p>
          <p><strong>Lot ID:</strong> {{ slot.lot_id }}</p>
          <p><strong>Label:</strong> {{ slot.label }}</p>
          <p><strong>Vehicle Number:</strong> {{ reservation.vehicle_number }}</p>
          <p><strong>Start Time:</strong> {{ reservation.start_time }}</p>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SlotDetailModal',
  props: {
    visible: { type: Boolean, default: false },
    slot: { type: Object, default: () => ({}) },
    reservation: { type: Object, default: () => ({}) }  
  }
}
</script>
