<template>
  <div class="p-3">
    <h5>{{ title }}</h5>
    <form @submit.prevent="onSave">
      <div v-for="field in fields" :key="field.key" class="mb-3">
        <label class="form-label">{{ field.label }}</label>

        <!-- DATETIME (show as text or inputs) -->
        <div v-if="field.type === 'datetime'">
          <div v-if="!editing[field.key]" class="d-flex gap-2 align-items-center">
            <span>{{ formatDate(localRow[field.key]) }}</span>
            <span>{{ formatTime(localRow[field.key]) }}</span>
            <button type="button" class="btn btn-sm btn-link"
                    @click="editing[field.key] = true">Edit</button>
          </div>

          <div v-else class="d-flex gap-2">
            <input v-model="localRow[field.key + '_date']" type="date" class="form-control" />
            <input v-model="localRow[field.key + '_time']" type="time" class="form-control" />
          </div>
        </div>

        <!-- OTHER TYPES -->
        <input v-else-if="field.type === 'text'" v-model="localRow[field.key]" type="text" class="form-control" />
        <div v-else-if="field.type === 'noedit'" class="form-control-plaintext">{{ localRow[field.key] }}</div>
        <input v-else v-model="localRow[field.key]" type="text" class="form-control" />
      </div>

      <div class="mt-3">
        <button type="submit" class="btn btn-primary">Save</button>
        <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue"

const props = defineProps({
  row: { type: Object, required: true },
  fields: { type: Array, required: true },
  title: { type: String, default: "Edit Record" }
})
const emit = defineEmits(["save", "cancel"])

const localRow = reactive({})
const editing = reactive({})

// Parse incoming datetime into date + time
function parseDateTime(val) {
  if (!val) return { date: "", time: "" }
  const d = new Date(val)
  if (isNaN(d)) return { date: "", time: "" }
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, "0")
  const dd = String(d.getDate()).padStart(2, "0")
  const hh = String(d.getHours()).padStart(2, "0")
  const min = String(d.getMinutes()).padStart(2, "0")
  return { date: `${yyyy}-${mm}-${dd}`, time: `${hh}:${min}` }
}

watch(
  () => props.row,
  (newRow) => {
    if (!newRow) return
    Object.assign(localRow, newRow)
    props.fields.forEach(f => {
      if (f.type === "datetime" && newRow[f.key]) {
        const { date, time } = parseDateTime(newRow[f.key])
        localRow[f.key + "_date"] = date
        localRow[f.key + "_time"] = time
        editing[f.key] = false
      }
    })
  },
  { immediate: true }
)

function formatDate(val) {
  if (!val) return ""
  const d = new Date(val)
  if (isNaN(d)) return ""
  return d.toLocaleDateString("en-GB") // dd/mm/yyyy
}

function formatTime(val) {
  if (!val) return ""
  const d = new Date(val)
  if (isNaN(d)) return ""
  return d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" })
}

function onSave() {
  const out = { ...localRow }
  props.fields.forEach(f => {
    if (f.type === "datetime") {
      const d = out[f.key + "_date"]
      const t = out[f.key + "_time"]
      if (d && t) {
        out[f.key] = `${d}T${t}:00` // recombine
      }
      delete out[f.key + "_date"]
      delete out[f.key + "_time"]
    }
  })
  emit("save", out)
}
</script>
