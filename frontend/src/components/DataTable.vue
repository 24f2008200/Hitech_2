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

<script>
export default {
  name: "DataTable",
  props: {
    columns: { type: Array, required: true },
    rows: { type: Array, required: true },
    enableFilters: { type: Boolean, default: true }
  },
  data() {
    return {
      filters: {}
    }
  },
  computed: {
    filteredRows() {
      return this.rows.filter(row =>
        Object.keys(this.filters).every(key =>
          !this.filters[key] || row[key] == this.filters[key]
        )
      );
    }
  },
  methods: {
    uniqueValues(key) {
      return [...new Set(this.rows.map(r => r[key]))].filter(v => v);
    }
  }
}
</script>
