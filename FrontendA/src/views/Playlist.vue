<!-- <template>
  <div>
    <h1>Playlist</h1>
    <ul>
      <li v-for="song in songs" :key="song.song_id">
        {{ song.song_name }}
        <button @click="addSongToPlaylist(song.song_id)" v-if="!isSongInPlaylist(song.song_id)">Add</button>
        <button @click="removeSongFromPlaylist(song.song_id)" v-else>Remove</button>
      </li>
    </ul>
    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const newSongName = ref('');
const songs = ref([]);
const playlistSongs = ref([]);

async function fetchSongsAndPlaylists() {
  try {
    const accessToken = localStorage.getItem('access_token');
    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };

    const songsResponse = await axios.get('http://127.0.0.1:5000/song', config);
    songs.value = songsResponse.data;

    const playlistsResponse = await axios.get('http://127.0.0.1:5000/playlist', config);
    playlistSongs.value = playlistsResponse.data.map(item => item.song_id);
  } catch (error) {
    console.error('Error fetching songs and playlists:', error);
  }
}

async function addSongToPlaylist(songId) {
  try {
    const accessToken = localStorage.getItem('access_token');
    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };

    const response = await axios.post('http://127.0.0.1:5000/playlist', { song_id: songId }, config);
    if (response.status === 200) {
      fetchSongsAndPlaylists(); // Update songs after adding a song to the playlist
    } else {
      console.error('Failed to add song to playlist:', response.data.message);
    }
  } catch (error) {
    console.error('Error adding song to playlist:', error);
  }
}

async function removeSongFromPlaylist(songId) {
  try {
    const accessToken = localStorage.getItem('access_token');
    const config = {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    };

    const response = await axios.delete(`http://127.0.0.1:5000/playlist/${songId}`, config);
    if (response.status === 200) {
      fetchSongsAndPlaylists(); // Update songs after removing a song from the playlist
    } else {
      console.error('Failed to remove song from playlist:', response.data.message);
    }
  } catch (error) {
    console.error('Error removing song from playlist:', error);
  }
}

function isSongInPlaylist(songId) {
  return playlistSongs.value.includes(songId);
}

onMounted(() => {
  fetchSongsAndPlaylists(); // Fetch songs and playlists when the component is mounted
});
</script> -->
