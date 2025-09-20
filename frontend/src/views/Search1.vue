<template>
  <DataTable
    :columns="columns"
    :rows="rows"
    @action-click="handleAction"
  />

  <!-- modal or inline -->
  <div v-if="showEditor" class="editor-wrapper">
    <!-- key forces Vue to recreate RowEditor when editingKey changes -->
<RowEditor
  :row="reservation"
  :fields="[
    { key: 'id', label: 'Reservation ID', type: 'noedit' },
    { key: 'start_time', label: 'Start Time', type: 'datetime' },
    { key: 'end_time', label: 'End Time', type: 'datetime' }
  ]"
  @save="updateReservation"
/>
  </div>
</template>

<script setup>

import { ref, onMounted, onUnmounted } from "vue";
import { apiFetch } from "../api";
import { useSearchStore } from "../stores/search";
import DataTable from "@/components/DataTable.vue";
import RowEditor from "@/components/RowEditor.vue";

const rows = ref([
  { id: 1, name: "Lot A", start_time: "Fri, 19 Sep 2025 10:15:19 GMT" },
  { id: 2, name: "Lot B", start_time: "Fri, 20 Sep 2025 09:30:00 GMT" }
])

const columns = [
  { key: "name", label: "Name" },
  { key: "start_time", label: "Start" },
  { key: "action1", label: "Edit", type: "action" }
]

const editingRow = ref(null)    // will hold the cloned row object
const editingKey = ref(null)    // unique key for RowEditor
const showEditor = ref(false)

const editorFields = [
  { key: 'name', label: 'Name', type: 'text' },
  { key: 'start_time', label: 'Start Time', type: 'datetime' }
]

// handle DataTable emitted action
// function handleAction({ action, id, row }) {
//   console.log('handleAction called', { action, id, row })

//   if (action === 'action1') {
//     // deep-clone so child receives a fresh object pointer
//     const clone = (typeof structuredClone === 'function')
//       ? structuredClone(row)
//       : JSON.parse(JSON.stringify(row))

//     editingRow.value = clone
//     // unique key forces full recreate in DOM
//     editingKey.value = `${row.id}-${Date.now()}`
//     showEditor.value = true

//     console.log('editingRow set', { editingRow: editingRow.value, editingKey: editingKey.value })
//   }
// }
function handleAction({ action, id, row }) {
  if (action === "action1") {
    const clone = JSON.parse(JSON.stringify(row)) // ✅ safe clone
    editingRow.value = clone
    editingKey.value = `${row.id}-${Date.now()}`
    showEditor.value = true
  }
}


function updateReservation(updated) {
  const idx = rows.value.findIndex(r => r.id === updated.id)
  if (idx !== -1) rows.value[idx] = updated
  closeEditor()
}

function closeEditor() {
  showEditor.value = false
  editingRow.value = null
  editingKey.value = null
}
</script>
