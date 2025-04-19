<template>
  <div>
    <form @submit.prevent="updateSong" class="add-song-form">
      <p v-if="errorMessage" class="error-message">{{errorMessage}}</p>
      
      <h2>Actions</h2>
      <div class="form-group">
        <label for="song_name">Song Name:</label>
        <input type="text" id="song_name" v-model="song_name" required>
      </div>
      <div class="form-group">
        <label for="lyrics">Lyrics:</label>
        <input type="text" id="lyrics" v-model="lyrics" required>
      </div>
      
      <div class="form-group">
        <label for="duration">Duration:</label>
        <input type="time" id="duration" v-model="duration" required>
      </div>
      <div class="form-group">
        <label for="genre">Genre:</label>
        <input type="text" id="genre" v-model="genre" required>
      </div>
      <div class="form-group">
        <label for="date_created">Date Created:</label>
        <input type="date" id="date_created" v-model="date_created" required>
      </div>
      <button type="submit" class="btn-addsong">Update</button>
      <!--<button @click.prevent="deleteSong" class="btn-delete">Delete</button> -->
    </form>
  </div>
</template>
<script setup>
import {ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import store from '../store';

const route=useRouter();
const song_id=route.currentRoute.value.params.id;
const song_name=ref('');
const duration=ref('');
const date_created = ref('');
const genre=ref('');
const lyrics=ref('');
const errorMessage=ref('');

onMounted(async() =>{
    try{
        const token=store.state.token;
        axios.defaults.headers.common['Authorization']=`Bearer ${token}`;
        const response=await axios.get('http://127.0.0.1:5000/song',{params:{song_id:song_id}});
        song_name.value=response.data.song_name;
        duration.value=response.data.duration;
        lyrics.value=response.data.lyrics;
        date_created=response.data.date_created;
        genre.value=response.data.genre;

        console.log(response.data);
    }
    catch(error)
    {
        console.error(error);
    }
});

async function updateSong(){
    try{
        const accessToken = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization']=`Bearer ${accessToken}`;
        const response=await axios.patch('http://127.0.0.1:5000/song',{
            song_name: song_name.value,
            duration:duration.value,
            lyrics:lyrics.value,
            date_created:date_created.value,
            genre:genre.value,
        },{
            params:{
                song_id:song_id
            }
        });
        console.log(response.data.message);
        route.push('/dashboard');
    }
    catch(error)
    {
        errorMessage.value='An error occurred during song updation. Please try again later.';
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
    max-width: 4000px;
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
    width: 50%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .btn-addsong {
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 6px;
    cursor: pointer;
    margin: 0 5px;
    border: none;
    color: #fff;
    background-color: #FF5722;
  }
  
  .btn-addsong:hover {
      filter: brightness(85%);
    }

    .btn-delete {
        background-color: #dc3545;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 6px;
        cursor: pointer;
        margin: 0 5px;
        border: none;
        color: #fff;
    }

    .btn-delete:hover {
        filter: brightness(85%);
    }
</style>
