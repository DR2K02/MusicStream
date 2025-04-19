<template>
    <div>
      <h2>Delete Song</h2>
      <p>Are you sure you want to delete this Song?</p>
      <button @click="deleteSong" class="btn-delete">Delete</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </template>
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';

  let errorMessage = ref('');
  const route = useRouter();
  const song_id = route.currentRoute.value.params.id;

  async function deleteSong() {
    try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    
    // Send song_id in JSON format as part of the request body
      const response = await axios.delete('http://127.0.0.1:5000/song', {
        data: { song_id: song_id }
      });

    // Handle success and show feedback to the user
      console.log(response.data.message);
      route.push('/dashboard');
    } catch (error) {
    // Handle error and show feedback to the user (e.g., toast message)
     errorMessage.value = 'An error occurred during Song deletion. Please try again later.';
      console.error(error);
    }
  }
</script>
