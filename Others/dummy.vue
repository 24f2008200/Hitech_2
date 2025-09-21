<script>
async function fetchProfile() {
  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch('/api/user/profile', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })

    if (!res.ok) throw new Error('Failed to load profile')

    const data = await res.json()
    Object.assign(profile, data)
  } catch (err) {
    console.error('fetchProfile error', err)
    serverError.value = err.message
  }
}

async function submit() {
  if (!validate()) return

  const payload = buildPayload()
  if (Object.keys(payload).length === 0) {
    successMsg.value = 'No changes to save.'
    return
  }

  saving.value = true
  serverError.value = ''
  successMsg.value = ''

  try {
    const token = localStorage.getItem('access_token')
    const res = await fetch('/api/user/profile', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {})
      },
      body: JSON.stringify(payload)
    })

    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.message || 'Failed to update profile')
    }

    const data = await res.json()
    Object.assign(profile, data)
    successMsg.value = 'Profile updated successfully.'
    editing.value = false
  } catch (err) {
    console.error('save profile error', err)
    serverError.value = err.message
  } finally {
    saving.value = false
    form.password = ''
    form.confirm_password = ''
  }
}
</script>