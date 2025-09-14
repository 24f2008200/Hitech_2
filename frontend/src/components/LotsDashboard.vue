<template>
  <div class="container mt-4">
    <h2 class="mb-3">Parking Lots Dashboard</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else class="row">
      <div class="col-md-6 mb-4" v-for="lot in lots" :key="lot.id">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ lot.name }}</h5>
            <p class="card-text">
              Price: ₹{{ lot.price }} per hour <br />
              Address: {{ lot.address }} <br />
              Pin Code: {{ lot.pin_code }}
            </p>

            <div class="d-flex flex-wrap">
              <button
                v-for="spot in lot.spots"
                :key="spot.id"
                class="btn m-1"
                :class="spot.status === 'A' ? 'btn-success' : 'btn-danger'"
              >
                {{ spot.label || ('Spot ' + spot.id) }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LotsDashboard",
  data() {
    return {
      lots: [],
      loading: true,
    };
  },
  async mounted() {
    try {
      const res = await fetch("http://localhost:5000/admin/lots");
      this.lots = await res.json();
    } catch (err) {
      console.error("Error fetching lots:", err);
    } finally {
      this.loading = false;
    }
  },
};
</script>
