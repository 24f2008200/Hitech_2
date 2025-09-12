app.component("admin-dashboard", {
  data() {
    return {
      lots: []
    };
  },
  mounted() {
    // Fetch parking lots from API
    fetch("/parking/dashboard", {
      headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    })
    .then(res => res.json())
    .then(data => { this.lots = data; });
  },
  template: `
    <div>
      <h3>Parking Lots</h3>
      <div class="d-flex flex-wrap">
        <parking-lot-card v-for="lot in lots" :key="lot.id" :lot="lot"></parking-lot-card>
      </div>
      <button class="btn btn-warning mt-3">+ Add Lot</button>
    </div>
  `
});
