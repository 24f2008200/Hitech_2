<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-96 relative">
      <h2 class="text-xl font-bold mb-4">Slot Details</h2>

      <p><strong>ID:</strong> {{ slot.id }}</p>
      <p><strong>Status:</strong>
        <span :class="slot.is_occupied ? 'text-red-600' : 'text-green-600'">
          {{ slot.is_occupied ? 'Occupied' : 'Available' }}
        </span>
      </p>
      <p><strong>Lot ID:</strong> {{ slot.lot_id }}</p>
      <p><strong>Number:</strong> {{ slot.number }}</p>

      <div class="mt-4 flex justify-end">
        <button
          class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
          @click="$emit('close')"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SlotDetailModal',
  props: {
    visible: { type: Boolean, default: false },
    slot: { type: Object, default: () => ({}) }
  }
}
</script>
