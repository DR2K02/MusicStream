<template>
    <div>
      <form @submit.prevent="handleSubmit" class="add-album-form">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  
        <h2>Add New Album</h2>
        <div class="form-group">
          <label for="album_name">Album Name:</label>
          <input type="text" id="album_name" v-model="album_name" required>
        </div>
        <div class="form-group">
          <label for="album_artist">Album Artist:</label>
          <input type="text" id="album_artist" v-model="album_artist" required>
        </div>
        <button type="submit" class="btn-addalbum">Add Album</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const album_name = ref('');
  const album_artist = ref('');
  let errorMessage = ref('');
  
  const router = useRouter();
  
  async function handleSubmit() {
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await axios.post('http://127.0.0.1:5000/album', {
       
        album_name: album_name.value,
        album_artist: album_artist.value,
      },{
      headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },});
      // Handle success and show feedback to the user (e.g., toast message)
      console.log('Album created:', response.data);
      router.push('/dashboard'); // Redirect to admin dashboard after successful creation
    } catch (error) {
      // Handle error and show feedback to the user (e.g., toast message)
      errorMessage.value = 'An error occurred during album creation. Please try again later.';
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
  
  .add-album-form {
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
  
  .btn-addalbum {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: #fff;
    text-align: center;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-addalbum:hover {
    filter: brightness(85%);
  }
  </style>
  