<template>
  <div class="container mt-4">
    <h2>Admin Search</h2>

    <div class="row mb-3">
      <div class="col-md-3">
        <select v-model="searchBy" class="form-select">
          <option disabled value="">Search By</option>
          <option value="name">Name</option>
          <option value="mobile">Mobile</option>
          <option value="address">Address</option>
          <option value="vehicles">Vehicles</option>
          <option value="driver">Driver Name</option>
          <option value="parking_lots">Parking Lots</option>
        </select>
      </div>

      <div class="col-md-5">
        <input type="text" v-model="searchValue" class="form-control" placeholder="Enter search value" />
      </div>

      <div class="col-md-2">
        <select v-model="searchType" class="form-select">
          <option value="users">Users</option>
          <option value="bookings">Bookings</option>
          <option value="payments">Payments</option>
          
        </select>
      </div>

      <div class="col-md-2">
        <button @click="performSearch" class="btn btn-primary w-100">
          Search
        </button>
      </div>
    </div>

    <!-- Results Table -->
    <div v-if="results.length > 0" class="mt-4">
      <h5>Results</h5>
      <table class="table table-striped">
        <thead>
          <tr>
            <th v-for="col in tableHeaders" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.id">
            <td v-for="col in tableHeaders" :key="col">
              {{ item[col] }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="searched" class="alert alert-warning">
      No results found.
    </div>
  </div>
</template>

<script>
import { apiFetch } from '../api'


export default {
  name: "SearchAdmin",
  data() {
    return {
      searchBy: "",
      searchValue: "",
      searchType: "users",
      results: [],
      searched: false,
      tableHeaders: []
    }
  },
  methods: {
    async performSearch() {
      if (!this.searchBy || !this.searchValue) {
        alert("Please select search by and enter a value.")
        return
      }

      try {
        const endpoint =
          this.searchType === "users"
            ? "/admin/search/users"
            : "/admin/search/bookings"

        const url = `${endpoint}?search_by=${this.searchBy}&value=${encodeURIComponent(this.searchValue)}`

        const response = await apiFetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("access_token")}` // if JWT is needed
          }
        })

        if (!response.ok) {
          throw new Error("Network response was not ok")
        }

        const data = await response.json()
        this.results = data
        this.searched = true

        if (this.results.length > 0) {
          this.tableHeaders = Object.keys(this.results[0])
        } else {
          this.tableHeaders = []
        }
      } catch (error) {
        console.error("Search error:", error)
        alert("Error fetching search results.")
      }
    }

  }
}
</script>
