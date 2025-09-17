<!-- Recent Parking History -->
<div class="card mb-4">
  <div class="card-header bg-primary text-white">
    Recent Parking History
  </div>
  <div class="card-body">
    <DataTable :columns="reservationColumns" :rows="reservations">
      <!-- Custom cell for From -->
      <template #start_time="{ row }">
        {{ f(row.start_time) }}
      </template>
      <!-- Custom cell for To -->
      <template #end_time="{ row }">
        {{ f(row.end_time) }}
      </template>
      <!-- Custom cell for Action -->
      <template #status="{ row }">
        <button v-if="row.status === 'active'"
                class="btn btn-sm btn-danger"
                @click="releaseSpot(row.id)">
          Release
        </button>
        <span v-else class="badge bg-success">Parked Out</span>
      </template>
    </DataTable>
  </div>
</div>
