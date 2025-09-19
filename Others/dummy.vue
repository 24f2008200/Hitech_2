<script setup>
import { ref } from "vue";
import { apiFetch } from "../api";
import { useSearchStore } from "../stores/search";  


const searchBy = ref("");
const searchValue = ref("");
const results = ref([]);
const searched = ref(false);
const tableHeaders = ref([]);


const searchStore = useSearchStore();
const searchType = searchStore.searchType; // reactive


async function performSearch() {
  if (!searchBy.value || !searchValue.value) {
    alert("Please select search by and enter a value.");
    return;
  }

  try {
    // Decide endpoint based on global searchType
    const endpoint =
      searchType === "user"
        ? "/admin/search/users"
        : searchType === "reservation"
        ? "/admin/search/bookings"
        : "/admin/search/lots";

    const url = `${endpoint}?search_by=${searchBy.value}&value=${encodeURIComponent(
      searchValue.value
    )}`;

    const response = await apiFetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    results.value = data;
    searched.value = true;

    if (results.value.length > 0) {
      tableHeaders.value = Object.keys(results.value[0]);
    } else {
      tableHeaders.value = [];
    }
  } catch (error) {
    console.error("Search error:", error);
    alert("Error fetching search results.");
  }
}
</script>

