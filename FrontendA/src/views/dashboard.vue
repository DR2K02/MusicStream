<template>
  
  
  <div>
      <section class="dashboard-container">
          <h3>Welcome, {{ user.name }}</h3>
          <!-- Creator Dashboard if the user is a creator -->
          <div v-if="user && user.is_creator">
            <router-link to="/search">Search Songs</router-link>
              <br>
              <h1 class="dashboard-heading">Creator Dashboard</h1>
              
              <router-link to="/add_album" class="btn btn-add-album">Add New Album</router-link>
              <br>
                <div class="dashboard-box">
                  <div v-for="album in user.albums" :key="album.album_id" class="album-card">
                    <h3>{{ album.album_name }}</h3>
                    <div class="album-buttons">
                      <router-link :to="{ name: 'Edit_album', params: { id: album.album_id }}" class="btn btn-edit">Edit</router-link>
                      <router-link :to="{ name: 'delete_album', params: { id: album.album_id }}" class="btn btn-delete">Delete</router-link>
                      <router-link :to="{ name: 'song_add', params: { id: album.album_id }}" class="btn btn-add-song">Add New Song</router-link>
                      
                    </div>
                    <button @click="exportAlbum(album.album_id)" class="btn btn-export">Export</button>
                    <hr class="dashboard-divider" />

            <div class="show-list">
              <div v-for="song in album.songs" :key="song.song_id" class="dashboard-song-card">
                <h4>{{ song.song_name }}</h4>
                <router-link :to="{ name: 'Edit_song', params: { id: song.song_id }}" class="btn btn-action">Edit</router-link>
                <router-link :to="{ name: 'Song_delete', params: { id: song.song_id }}" class="btn btn-delete">Delete</router-link>
                <router-link to="/rate_song"> Rate Songs</router-link>
              </div>
            </div>
                </div>
                </div>

            
              
              
          </div>
          <!-- Admin Dashboard if the user is an admin -->
          <div v-else-if="user && user.is_admin">
              <h1 class="dashboard-heading">Admin Dashboard</h1>
              <h2>Creator Requests Till Now</h2>
              <ul>
                  <li v-for="user in creatorRequests" :key="user.id">
                      <span>{{ user.email }}</span>
                      <button @click="approveCreator(user.id)">Approve</button>
                      <button @click="rejectCreator(user.id)">Reject</button>
                  </li>
              </ul>

              <div v-if="creatorStats" class="creator-stats">
                <h2>Creator Statistics</h2>
                <div v-for="(creator,index) in creatorStats.creator_stats":key="index">
                  <div>
                    <strong>User ID:</strong> {{ creator.user_id }}
                  </div>
                  <div>
                    <strong>Name:</strong> {{ creator.name }}
                  </div>
                <div>
                    <strong>Number of Albums:</strong> {{ creator.num_albums }}
                </div>
                <div>
                    <strong>Number of Songs:</strong> {{ creator.num_songs }}
                </div>
                <div>
                    <strong>Average Rating:</strong> {{ creator.avg_rating }}
                </div>
              <br>  
            </div>
            <div class="total-creators">
              <strong>Number of Creators:</strong> {{ creatorStats.num_creators }}
            </div>
            </div>
              
          </div>
          <!-- Show the user dashboard if the user is a normal user -->
          <div v-else>
              <h1 class="dashboard-heading">User Dashboard</h1>
              <!-- Display a button to request creator access -->
              <router-link to="/search">Search Songs</router-link>
              <div v-if="songs.length">
                <ul>
                  <li v-for="song in songs" :key="song.song_id">
                    <p><strong>Song Name:</strong> {{ song.song_name }}</p>
                    <p><strong>Lyrics:</strong></p>
                    <div class="lyrics-container">
                      <pre class="lyrics">{{ song.lyrics }}</pre>
                    </div>
                    <p><strong>Rating:</strong> {{ song.average_rating }}</p>
                    <p><strong>Genre:</strong> {{ song.genre }}</p>
                    <p><strong>Duration:</strong> {{ song.duration }}</p>
                    <p><strong>Date Created:</strong> {{ song.date_created }}</p>
                    <p><strong>Album Name:</strong> {{ song.album_name }}</p>
                    <p><strong>Album Artist:</strong> {{ song.album_artist }}</p>
                  
                    
                    
                    <!-- You can include more details if needed -->
                  </li>
                </ul>
                
              </div>
              <p v-else>No songs available</p>
              <h4>Request to Become a Creator</h4>
              <button class="request-button" @click="requestCreatorAccess">Request</button>
              <br>
              <router-link to="/rate_song"> Rate Songs</router-link>
              <br>
              
              
              <div>
              
              
        </div>
          
        </div>
      </section>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from 'vue-router';

const route = useRoute(); 
const user = ref("");
const creatorRequests = ref([]);
const creatorStats = ref(null);
let errorMessage = ref("");
const selectedSong=ref(null);
const rating = ref("");
const songs = ref([]);


const fetchData = async () => {
  try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const response = await axios.get("http://127.0.0.1:5000/home");
      user.value = response.data;
      if (user.value && user.value.is_admin) {
          await fetchCreatorRequests();
          await fetchCreatorStats();
      }
      const songsResponse=await axios.get('http://127.0.0.1:5000/song');
      songs.value=songsResponse.data;
      localStorage.setItem('user', JSON.stringify(user.value));
  } catch (error) {
      errorMessage.value = "An error occurred during user fetch. Please try again later.";
      console.error(error);
  }
};

const fetchCreatorStats = async () => {
  try {
      const token = localStorage.getItem('access_token');
      //const user_id = localStorage.getItem('user_id');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const response = await axios.get(`http://127.0.0.1:5000/stats`); // Replace '5' with the actual user ID
      creatorStats.value = response.data;
  } catch (error) {
      errorMessage.value = "An error occurred while fetching creator statistics. Please try again later.";
      console.error(error);
  }
};


const fetchCreatorRequests = async () => {
  try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const response = await axios.get("http://127.0.0.1:5000/creator_requests");
      creatorRequests.value = response.data;
  } catch (error) {
      errorMessage.value = "An error occurred while fetching creator requests. Please try again later.";
      console.error(error);
  }
};


async function exportAlbum(album_id) {

try {
  const token = localStorage.getItem('access_token');
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  const response = await axios.get(`http://127.0.0.1:5000/export`, {params: {album_id: album_id}});

  // Handle success and show feedback to the user
  console.log(response.data.message);
  fetchData();
} 
catch (error) {

  errorMessage.value = 'An error occurred during album export. Please try again later.';
  console.error(error);
}
}
async function requestCreatorAccess() {
  try {
      console.log('Requesting creator access...');
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      // Make an HTTP POST request to the backend API endpoint
      const response = await axios.post('http://127.0.0.1:5000/become_creator');
      console.log('Creator access requested successfully:', response.data);
      // Optionally, you can update the UI or display a success message
  } catch (error) {
      console.error('Error requesting creator access:', error);
      // Handle errors (e.g., display an error message to the user)
  }
}

const approveCreator = async (userId) => {
  try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const response = await axios.put(`http://127.0.0.1:5000/approve_creator/${userId}`, { action: 'approve' });
      console.log('Creator request approved:', response.data);
      await fetchCreatorRequests();
  } catch (error) {
      console.error('Error approving creator request:', error);
      errorMessage.value = "An error occurred while approving creator request. Please try again later.";
  }
};

const rejectCreator = async (userId) => {
  try {
      const token = localStorage.getItem('access_token');
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const response = await axios.put(`http://127.0.0.1:5000/approve_creator/${userId}`, { action: 'reject' });
      console.log('Creator request rejected:', response.data);
      await fetchCreatorRequests();
  } catch (error) {
      console.error('Error rejecting creator request:', error);
      errorMessage.value = "An error occurred while rejecting creator request. Please try again later.";
  }
};




onMounted(() => {
  fetchData();
  fetchCreatorStats();
});


</script>



<style scoped>
/* Add your styles here */
button {
  padding: 8px 16px; /* Increase the padding for the buttons */
}
.lyrics-container {
  border: 2px solid #4CAF50; /* Green border */
  border-radius: 10px;
  padding: 10px;
  background-color: #f8f8f8;
  overflow: auto;
  max-height: 200px; /* Adjust as needed */
}

.lyrics {
  white-space: pre-wrap;
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
}
  .request-button{
      background-color: #4CAF50; /* Green */
      border: none;
      color: white;
      padding: 10px 20px;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: 16px;
      margin: 4px 2px;
      transition-duration: 0.4s;
      cursor: pointer;
      border-radius: 5px;
  }

  .request-button:hover{
      background-color: #45a049; /* Darker Green */
  }

  .admin-dashboard {
    padding: 20px;
    background-color: #f5f5f5;
}

.dashboard-heading {
    font-size: 24px;
    margin-bottom: 20px;
}

.creator-stats {
  margin-top: 20px;
}

.creator-stat-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.creator-stat-item div {
  margin-bottom: 5px;
}

.total-creators {
  margin-top: 20px;
  font-weight: bold;
}

</style>
