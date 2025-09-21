import { defineStore } from "pinia";
import { ref } from "vue";

export const useSearchStore = defineStore("search", () => {
  // state
  const searchType = ref("user");     // default
  const searchValue = ref("");   // default
  const navbarAction = ref(null);     // will hold a function

  // actions
  function setSearchType(type) {
    searchType.value = type;
  }

  function setSearchValue(nValue) {
    searchValue.value = nValue;
  }

  function setNavbarAction(actionFn) {

    navbarAction.value = actionFn;
  }

  function triggerNavbarAction() {
    if (navbarAction.value) {
      navbarAction.value();
    } else {

    }
  }

  // expose
  return {
    searchType,
    searchValue,
    navbarAction,
    setSearchType,
    setSearchValue,
    setNavbarAction,
    triggerNavbarAction
  };
});
