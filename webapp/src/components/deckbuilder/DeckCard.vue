<template>
  <div class="deck-card">
    <img :src="card.image" />
    <span>{{ card.name }}</span>
    <button @click="$emit('remove')">X</button>
  </div>
</template>

<script setup>
defineProps({
  card: Object
})
</script>

<style>
.deck-card {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.deck-card img {
  width: 40px;
}
</style>