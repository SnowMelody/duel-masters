<template>
  <div
    class="card-item"
    draggable="true"
    @dragstart="onDrag"
    @click="$emit('add')"
  >
    <img :src="card.image" />
    <div class="name">{{ card.name }}</div>
  </div>
</template>

<script setup>
const props = defineProps({
  card: Object
})

function onDrag(e) {
  e.dataTransfer.setData("card", JSON.stringify(props.card))
}
</script>

<style>
.card-item {
  cursor: grab;
}

.card-item img {
  width: 100%;
  border-radius: 8px;
}
</style>