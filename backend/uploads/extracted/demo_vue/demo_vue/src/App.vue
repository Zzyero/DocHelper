<script setup>
import { onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

// 初始化粒子效果
let scene, camera, renderer, particles
let animationId = null

onMounted(() => {
  initParticleEffect()
  window.addEventListener('resize', onWindowResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onWindowResize)
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (renderer) {
    const container = document.querySelector('.particles')
    if (container && container.contains(renderer.domElement)) {
      container.removeChild(renderer.domElement)
    }
  }
})

function initParticleEffect() {
  const container = document.querySelector('.particles')
  if (!container) return

  // 创建场景
  scene = new THREE.Scene()
  
  // 创建相机
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  camera.position.z = 30
  
  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ 
    antialias: true,
    alpha: true 
  })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  container.appendChild(renderer.domElement)
  
  // 创建粒子
  const particlesGeometry = new THREE.BufferGeometry()
  const particleCount = 1500
  
  const posArray = new Float32Array(particleCount * 3)
  const scaleArray = new Float32Array(particleCount)
  
  for (let i = 0; i < particleCount * 3; i += 3) {
    // 位置
    posArray[i] = (Math.random() - 0.5) * 80
    posArray[i + 1] = (Math.random() - 0.5) * 80
    posArray[i + 2] = (Math.random() - 0.5) * 80
    
    // 大小
    scaleArray[i / 3] = Math.random()
  }
  
  particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  particlesGeometry.setAttribute('scale', new THREE.BufferAttribute(scaleArray, 1))
  
  // 材质
  const particlesMaterial = new THREE.PointsMaterial({
    size: 0.2,
    sizeAttenuation: true,
    color: 0x4fc3f7,
    transparent: true,
    opacity: 0.8
  })
  
  // 创建粒子系统
  particles = new THREE.Points(particlesGeometry, particlesMaterial)
  scene.add(particles)
  
  animate()
}

function animate() {
  animationId = requestAnimationFrame(animate)
  
  particles.rotation.x += 0.0005
  particles.rotation.y += 0.0005
  
  renderer.render(scene, camera)
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
}
</script>

<template>
  <div class="app-container">
    <div class="background-effects">
      <div class="gradient-bg"></div>
      <div class="particles"></div>
    </div>
    <router-view v-slot="{ Component }" class="router-view-container">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style>
.app-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.gradient-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.router-view-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
