import { defineStore } from "pinia";

export const useSearchStore = defineStore("search", {
  state: () => ({
    searchType: "user", // default
  }),
  actions: {
    setSearchType(type) {
      this.searchType = type;
    },
  },
});
