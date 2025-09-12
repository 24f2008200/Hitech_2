app.component("parking-lot-card", {
  props: ["lot"],
  template: `
    <div class="card m-2" style="width: 18rem;">
      <div class="card-body">
        <h5 class="card-title"> {{ lot.name }} </h5>
        <p class="card-text">
          Occupied: {{ lot.occupied }} / {{ lot.total }}
        </p>
        <button class="btn btn-sm btn-primary me-2">Edit</button>
        <button class="btn btn-sm btn-danger">Delete</button>
        <div class="mt-2 d-flex flex-wrap">
          <div v-for="spot in lot.spots"
            :class="['m-1', 'rounded-circle', spot.is_occupied ? 'bg-danger' : 'bg-success']"
            style="width: 20px; height: 20px;">
          </div>
        </div>
      </div>
    </div>
  `
});
