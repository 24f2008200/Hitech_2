<template>
  <div class="container mt-5">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary" type="submit">Login</button>
    </form>
    <p v-if="error" class="text-danger mt-2">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
      error: ""
    }
  },
  methods: {
    async login() {
      try {
        const res = await fetch("http://localhost:5000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include", // send cookies/session
          body: JSON.stringify({ email: this.email, password: this.password })
        })
            console.log("Raw response:", res)

            const data = await res.json().catch(() => null)
            console.log("Parsed data:", data)
        if (!res.ok) {
          const errData = await res.json()
          this.error = errData.message
          return
        }
                 // Store JWT + role
        localStorage.setItem("access_token", data.access_token)
        localStorage.setItem("is_admin", data.user.is_admin)
        if (data.role === "admin") {
          this.$router.push("/admin")
        } else {
          this.$router.push("/user")
        }
      } catch (err) {
        console.error("Login failed:", err)
        this.error = "Something went wrong."
      }
    }
  }
}
</script>
