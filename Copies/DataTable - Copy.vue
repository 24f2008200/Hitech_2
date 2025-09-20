
<template>
  <div>
    <table class="table table-striped align-middle text-center">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" class="px-2 py-2">
            {{ col.label }}
            <div v-if="enableFilters" class="mt-1">
              <select v-model="filters[col.key]" class="form-select form-select-sm w-auto mx-auto">
                <option value="">All</option>
                <option
                  v-for="opt in uniqueValues(col.key)"
                  :key="opt"
                  :value="opt"
                >
                  {{ opt }}
                </option>
              </select>
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in filteredRows" :key="row.id">
          <td v-for="col in columns" :key="col.key" class="px-2 py-1">
            <slot :name="col.key" :row="row">{{ row[col.key] }}</slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Use props safely by assigning const props = defineProps(...)
const props = defineProps({
  columns: { type: Array, required: true },
  rows: { type: Array, required: true },
  enableFilters: { type: Boolean, default: true }
})

// reactive filters
const filters = ref({})

// computed filteredRows uses props.rows and filters.value
const filteredRows = computed(() => {
  // if rows is undefined, return empty array safely
  const rows = props.rows || []
  return rows.filter(row =>
    Object.keys(filters.value).every(key =>
      !filters.value[key] || row[key] === filters.value[key]
    )
  )
})

// helper to get unique, non-empty values for a column
function uniqueValues(key) {
  const rows = props.rows || []
  return [...new Set(rows.map(r => r[key]).filter(v => v !== null && v !== undefined && v !== ""))]
}
</script>
