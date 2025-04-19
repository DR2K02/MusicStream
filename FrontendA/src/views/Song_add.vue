<template>
  <div>
    <form @submit.prevent="handleSubmit" class="add-song-form">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <h2>Add New Song</h2>
      <div class="form-group">
        <label for="song_name">Song Name:</label>
        <input type="text" id="song_name" v-model="song_name" required>
      </div>
      <div class="form-group">
        <label for="lyrics">Lyrics:</label>
        <input type="text" id="lyrics" v-model="lyrics" required>
      </div>
      <div class="form-group">
        <label for="date_created">Date Created:</label>
        <input type="date" id="date_created" v-model="date_created" required>
      </div>
      <div class="form-group">
        <label for="duration">Duration:</label>
        <input type="time" id="duration" v-model="duration" required>
      </div>
      <div class="form-group">
        <label for="genre">Genre:</label>
        <input type="text" id="genre" v-model="genre" required>
      </div>
      <button type="submit" class="btn-addsong">Add Song</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const route = useRouter();

const song_name = ref('');
const lyrics = ref('');
const genre = ref('');
const duration = ref('');
const date_created = ref('');

const album_id = route.currentRoute.value.params.id;

let errorMessage = ref('');

async function handleSubmit() {
  try {
    const accessToken = localStorage.getItem('access_token');
    const response = await axios.post('http://127.0.0.1:5000/song', {
      song_name: song_name.value,
      lyrics: lyrics.value,
      genre: genre.value,
      album_id: album_id,
      duration: duration.value,
      date_created: date_created.value,
    },{
      headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },});
    console.log(response.data.message);
    route.push('/dashboard');
  } catch (error) {
    errorMessage.value = 'An error occurred during song creation. Please try again later';
    console.error(error);
  }
}
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

.add-song-form {
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

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-addsong {
  width: 100%;
  padding: 10px;
  background-color: #FF5722;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-addsong:hover {
  background-color: #e64a19;
}
</style>
