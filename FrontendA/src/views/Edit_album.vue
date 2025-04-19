<template>
    <div>
        <form @submit.prevent="updateAlbum" class="add-album-form">
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            
            <h2>Edit Album</h2>
            <div class="form-group">
                <label for="album_name">Album Name:</label>
                <input type="text" id="album_name" v-model="album_name" required>

            </div>
            <div class="form-group">
                <label for="album_artist">Album Artist:</label>
                <input type="text" id="album_artist" v-model="album_artist" required>

            </div>
            <button type="submit" class="btn-addalbum">Update</button>
        </form>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import store from '../store';

const album_name=ref('');
const artist=ref('');
let errorMessage=ref('');

const route=useRouter();
const album_id=route.currentRoute.value.params.id;

onMounted(async () => {
    try{
        const token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization']=`Bearer ${token}`;
        const response=await axios.get('http://127.0.0.1:5000/album',{params:{album_id:album_id}});
        album_name.value=response.data.album_name;
        album_artist.value=response.data.album_artist;

        console.log(response.data);
    }
    catch(error)
    {
        console.error(error);
    }
});
async function updateAlbum(){
    try{
        const token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization']=`Bearer ${token}`;
        const response =await axios.patch('http://127.0.0.1:5000/album',{
            album_name:album_name.value,
            album_artist:album_artist.value,

        },{
            params:{
                album_id:album_id
            }
        });
        console.log(response.data.message);
        route.push('/dashboard');
    }
    catch (error)
    {
        errorMessage.value='An error occurred during album updation. Please try again later.';
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

.btn-addalbum {
  width: 10%;
  padding: 10px;
  background-color: #FF5722;
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
  