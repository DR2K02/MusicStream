import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Dashboard from '../views/dashboard.vue'
import Album_add from '../views/Album_add.vue'
import Edit_album from '../views/Edit_album.vue'
import delete_album from '../views/Album_delete.vue'
import song_add from '../views/Song_add.vue'
import Edit_song from '../views/Edit_song.vue'
import Song_delete from '../views/Song_delete.vue'
//import Playlist from '../views/Playlist.vue'
import Search from '../views/Search.vue'
import RateSong from '../views/RateSong.vue'
//import SongList from '../views/SongList.vue'
import store from '../store/index.js'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path:'/login',
      name:'login',
      component:Login
    },
    {
      path:'/signup',
     name:'signup',
    component:Signup
  },
  {
      path:'/dashboard',
      name:'dashboard',
      component:Dashboard,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
      
    },
    
   {
      path:'/add_album',
      name:'Album_add',
      component:Album_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
      
    },
    
    {
      path:'/edit_album/:id',
      name:'Edit_album',
      component: Edit_album,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
      
    },
    {
      path:'/delete_album/:id',
      name:'delete_album',
      component: delete_album,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
      
    },
    
    {
      path:'/add_song/:id',
      name:'song_add',
      component:song_add,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
      
    },
    
    {
      path:'/edit_song/:id',
      name:'Edit_song',
      component: Edit_song,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    {
      path:'/delete_song/:id',
      name:'Song_delete',
      component: Song_delete,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    },
    
    // {
    //   path:'/playlist',
    //   name:'Playlist',
    //   component:Playlist,
      
    // },

    {
      path:'/search',
      name:'Search',
      component:Search,
    },
    {
      path:'/rate_song',
      name:'RateSong',
      component:RateSong,
      meta: {
        requiresAuth: true, // meta field to indicate that the route requires authentication
      }
    }

    
  ]
})

router.beforeEach((to,from,next)=>{
  if (to.meta.requiresAuth && !store.state.token){
    next('/login');
  }
  else if (from.name ==='dashboard' && (to.name==='login' || to.name ==='signup')){
    store.dispatch('logout').then(()=>{
      next();
    }).catch((error)=>{
      console.error('Logout failed:',error);
      next();
    });
  }
  else{
    next();
  }
});
export default router
