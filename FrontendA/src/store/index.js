import {createStore} from 'vuex';
import axios from 'axios';
const store=createStore({
  state:{
    token:null,
    user:null,
  },
  mutations:{
    setToken(state,token)
    {
      state.token=token;
      localStorage.setItem('token',token);
    },
    setUser(state,user)
    {
      state.user=user;
    },
  },
  actions:{
    login({commit},{token,user})
    {
      commit('setToken',token);
      commit('setUser',user);
    },
    async logout({commit}){
      try{
        const token=store.state.token;
        axios.defaults.headers.common['Authorization']=`Bearer ${token}`;
        await axios.post('http://127.0.0.1:5000/logout');
        commit('setToken',null);
        localStorage.removeItem('token');
        localStorage.removeItem('is_creator')
        localStorage.removeItem('user_id')
        localStorage.removeItem('access_token')
        commit('setUser',null);
      }
      catch(error)
      {
        console.error('Logout failed:',error);
      }
    },
  }

});

export default store;