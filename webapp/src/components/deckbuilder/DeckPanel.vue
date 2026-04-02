<template>
  <div
    class="deck-panel"
    @dragover.prevent
    @drop="onDrop"
  >
    <DeckCard
      v-for="(card, index) in deck"
      :key="index"
      :card="card"
      @remove="$emit('remove', index)"
    />

    <div class="count">Total: {{ deck.length }}</div>
  </div>
</template>

<script setup>
import DeckCard from "./DeckCard.vue"

const props = defineProps({
  deck: Array
})

const emit = defineEmits(["remove","add"])

function onDrop(e) {
  const card = JSON.parse(e.dataTransfer.getData("card"))
  emit("add", card)
}
</script>

<style>
.deck-panel {
  border-left: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
}

.count {
  margin-top: 10px;
  font-weight: bold;
}
</style>