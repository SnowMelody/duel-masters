<template>
  <div class="card-grid">
    <CardItem
      v-for="card in cards"
      :key="card.id"
      :card="card"
      @add="$emit('add', card)"
    />
  </div>
</template>

<script setup>
import CardItem from "./CardItem.vue"

defineProps({
  cards: Array
})
</script>

<style>
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 8px;
  padding: 10px;
  overflow-y: auto;
}
</style>