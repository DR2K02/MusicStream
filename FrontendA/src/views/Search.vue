<template>
  <div>
    <h1>Song Search</h1>
    <input v-model="searchQuery" type="text" placeholder="Enter search query">
    <button @click="searchSongs">Search</button>
    
    <div v-if="isLoading">Searching...</div>
    
    <div v-if="!isLoading && songs.length === 0">
      No songs found.
    </div>
    
    <div v-if="songs.length > 0">
      <h2>Search Results</h2>
      <ul>
        <li v-for="song in songs" :key="song.song_id">
          <div>{{ song.song_name }}</div>
          <div>Album: {{ song.album_name }}</div>
          <div>Artist: {{ song.album_artist }}</div>
          <div>Rating: {{ song.average_rating }}</div>
          <div>Genre: {{ song.genre }}</div>
          <div>Duration: {{ song.duration }}</div>
          <div>Lyrics: {{ song.lyrics }}</div>
        </li>
      </ul>
    </div>
    
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const songs = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

const searchSongs = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('Access token not found')
    }

    const response = await axios.get('http://127.0.0.1:5000/search', {
      params: { searchQuery: searchQuery.value },
      headers: { Authorization: `Bearer ${token}` }
    })

    songs.value = response.data.songs
  } catch (error) {
    errorMessage.value = 'An error occurred while fetching search results'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>
