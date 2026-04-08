import { mount } from 'svelte'
import './app.css'
import App from './lib/components/App.svelte'

//Target
const appTarget = document.getElementById('app');
const instances = {};

if (appTarget) {
  instances.app = mount(App, { target: appTarget });
} else {
  console.warn('#app not found');
}

export default instances;