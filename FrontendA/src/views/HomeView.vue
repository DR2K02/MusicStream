<script setup>
</script>

<template>
  <section class="about">
    <div class="container">
      <h2> Sangeet</h2>
      <p> Sangeet is a popular music streaming app offering a vast library of songs across multiple genres, along with curated personalized recommendations, providing users with a seamless music listening experience on-the-go. </p>
    </div>
  </section>
  <section class="featured-songs">
    <div class="container">
      <h2> Featured Songs</h2>
      <div class="song-list">
      <div class="song-card">
        <img src="../assets/Asal-Mein.jpg" alt="Asal Mein">
        <h3>Asal Mein</h3>
        <p>Genre: Romantic</p>
        <p>Artist: Darshan Raval</p>
        <p>Lyrics:Gurpreet Saini,Gautam Sharma</p>
        <p>Release Date:Feb 14,2020</p>
      </div>
      <div class="song-card">
        <img src="../assets/jeena.jpg" alt="Jeena Jeena">
        <h3>Jeena Jeena</h3>
        <p>Genre: Romantic</p>
        <p>Artist: Atif Aslam</p>
        <p>Lyrics:Dinesh Vijan,Priya Saraiya</p>
        <p>Release Date:Jan 14,2015</p>
        
      </div>
      <div class="song-card">
        <img src="../assets/Lut-Gaye.jpg" alt="Lut Gaye">
        <h3>Lut Gaye</h3>
        <p>Genre: Romantic</p>
        <p>Artist: Jubin Nautiyal</p>
        <p>Lyrics:Manoj Muntashir</p>
        <p>Release Date:Feb 17,2021</p>
        
        
      </div>
      <div class="song-card">
        <img src="../assets/phir_bhi.jpg" alt="Phir Bhi Tumko Chahunga">
        <h3>Phir Bhi Tumko Chahunga</h3>
        <p>Genre: Romantic</p>
        <p>Artist: Arijit Singh</p>
        <p>Lyrics:Manoj Muntashir</p>
        <p>Release Date:April 14,2017</p>
      </div>
    </div>
    </div>
  </section>
  
</template>
<script setup>
// Import the song path


</script>
<style>
.about {
  background-color:bisque;
  padding: 50 px 0;
}
.featured-songs {
  padding: 50 px 0;
}
.song-list {
  display: flex;
  justify-content: space-between;
}

.song-card {
  width: 30%;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.song-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  margin-bottom: 20px;
}

.song-card h3 {
  margin-top: 0;
}

.song-card p {
  margin-bottom: 10px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #FF5722;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}

</style>
