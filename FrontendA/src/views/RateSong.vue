<template>
  <div>
    <form @submit.prevent="handleSubmit" class="rate-song-form">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <h2>Rate Song</h2>
      <div class="form-group">
        <label for="song">Song:</label>
        <select v-model="selectedSong" id="song" required>
          <option value="" disabled>Select a song</option>
          <option v-for="song in songs" :key="song.song_id" :value="song.song_id">{{ song.song_name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="rating">Rating:</label>
        <input type="number" id="rating" v-model="rating" min="1" max="5" required>
      </div>
      <button type="submit" class="btn-rate-song">Rate Song</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const rating = ref('');
const selectedSong = ref('');
const errorMessage = ref('');
const songs = ref([]);

// Fetch songs
const fetchSongs = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/song');
    songs.value = response.data;
  } catch (error) {
    errorMessage.value = 'An error occurred while fetching songs. Please try again later';
    console.error(error);
  }
}

async function handleSubmit() {
  try {
    console.log(selectedSong.value)
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.post(`http://127.0.0.1:5000/rate_song`, {
      song_id:selectedSong.value,
      rating: parseInt(rating.value)
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    console.log(response.data.message);
    router.push('/dashboard');
    // Optionally, update UI or display a success message
  } catch (error) {
    errorMessage.value = 'An error occurred while adding rating. Please try again later';
    console.error(error);
  }
}

fetchSongs();
</script>

<style>
.error-message {
  color: #dc3545;
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
  text-align: center;
}

.rate-song-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f1f1f1;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-rate-song {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-rate-song:hover {
  background-color: #0056b3;
}
</style>
