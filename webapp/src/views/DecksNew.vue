<template>

  
  <div>
    <!--
    <div v-show="warning" @click="closeOverlay()" class="overlay"></div>

    

    <div v-show="warning" class="error">
      <p class="text-block">{{ warning }}</p>
      <div @click="warning = ''" class="btn">Close</div>
    </div>

    <div v-if="showWizard" class="new-duel">
      <div class="backdrop" @click="showWizard = false"></div>
      <div class="wizard">
        <div class="spacer">
          <span class="headline">Edit your deck</span>
          <br /><br />
          <form>
            <span class="helper">Name</span>
            <input v-model="selectedDeck.name" type="text" placeholder="Name" />
            <br /><br />

            <span class="helper">Visibility</span>
            <select v-model="selectedDeck.public">
              <option :value="true">Public</option>
              <option :value="false">Private</option>
            </select>

            <div @click="showWizard = false" class="btn">Done</div>
          </form>
        </div>
      </div>
    </div>

    <Header>
    </Header>

  -->
    
  <!--
    <div class="deck-top-bar">
      <span class="deck-card-total" v-if="selectedDeck">
        ({{selectedDeck.cards.length}})
      </span>

      <select v-model="selectedDeckUid">
        <option
          v-for="(deck, index) in decks"
          :key="index"
          :value="deck.uid"
        >
          {{ deck.name }}
        </option>
      </select>

      <div class="deck-secondary-buttons">

      </div>

      <div class="deck-crud-buttons">
        <div @click="newDeck()" class="btn new">NEW DECK</div>

        <template
          v-if="
            selectedDeck && deckCopy &&
            !decksEqual(selectedDeck, deckCopy)
          "
        >
          <div @click="save()" class="btn save">Save</div>
          <div @click="discard()" class="btn discard">Discard</div>
        </template>
      </div>
    </div>
  -->

    <span v-if="previewCard">
      <div 
        class="card-preview" 
        :style="{
          top: previewCardTop + 'px',
          left: previewCardLeft + 'px',
          width: previewCardWidth + 'px',
          height: previewCardHeight + 'px'
        }"
      >
        <img 
          :src="`/assets/cards/${previewCard.uid}.jpg`" 
          :alt="previewCard.name"
        />
      </div>
    </span>

    <div class="main">
      <!-- Deck builder area -->
      <div
        name="deck-reorder"
        tag="div"
        class="deck-panel"
        @dragover.prevent
        @drop="onBuilderDropEmpty"
      >
        <div
          v-for="(card, index) in getCardsForDeck(selectedDeck.cards)"
          :key="index"
          class="deck-card-slot"
          draggable="true"
          @dragstart="onBuilderDragStart(index)"
          @dragover.prevent="onBuilderDragOver(index, $event)"
          @drop="onBuilderDrop(index)"
          :class="{
            dragging: index === draggedCardIndex,
            'drop-left': dragOverIndex === index && dropSide === 'left',
            'drop-right': dragOverIndex === index && dropSide === 'right'
          }"
          @mouseleave="previewCard = null"
        >
          <div
            class="deck-card-oval"
            :class="'card-' + card.civilization.toLowerCase()"
            @click="tryRemoveCard(card)"
          >
            <v-lazy-image
              :src="`/assets/cards/${card.uid}.jpg`"
              src-placeholder="/assets/cards/backside.jpg"
              :alt="card.name"
            />
          </div>
        </div>
      </div>

      <!-- Card catalogue area -->
      <div class="catalogue-cards-wrapper">
        <div class="catalogue-cards">
          <div
            v-for="card in filteredAndSortedCards"
            :key="card.uid"
            class="catalogue-card"
            @click="tryAddCard(card)"
            draggable="true"
            @dragstart="onCatalogueDragStart(card)"
            @mouseover="showPreview(card, $event)"
            @mouseleave="hidePreview"
          >
            <v-lazy-image :src="`/assets/cards/${card.uid}.jpg`" />
          </div>
        </div>
      </div>

      <!-- Card search area -->
      <div class="catalogue-search">
        <input
          v-model="filterCard"
          type="search"
          placeholder="Search cards by name"
        />

        <button
          class="filter-button"
          @click="toggleFilter"
        >
          Filter
        </button>

        <button
          class="filter-button"
          @click="toggleSort"
        >
          Sort
        </button>
      </div>
    </div>

    <!-- Filter Popup area -->
    <div v-if="showFilterPopup" class="filter-popup-overlay">
      <div class="filter-popup">
        <button class="filter-close" @click="closeFilter">
          ✕
        </button>

        <div class="filter-popup-content">
          <div class="filter-section">
            
            <!-- Civilization Filter -->
            <div class="filter-title">
              Civilization
            </div>
            <div class="civ-icons">
                <div
                  v-for="civ in ['light','water','darkness','fire','nature']"
                  :key="civ"
                  class="civ-filter"
                  :class="[
                    'civ-color-' + civ,
                    selectedCivilizations.includes(civ) ? 'civ-filter-selected' : ''
                  ]"
                  @click="toggleCivilization(civ)"
                >
              </div>
            </div>

            <!-- Type Filter -->
            <div class="filter-title">
              Type
            </div>
            <div>
              <select 
                class="catalogue-filter"
                v-model="filterFamily">
                <option
                  class="family"
                  v-for="(family, index) in families"
                  :key="index"
                  :value="family"
                  >{{ family }}</option
                >
              </select>
            </div>

            <!-- Mana Filter -->
            <div class="filter-title">
              Mana
            </div>
            <div 
              v-for="manaNr in ['1', '2', '3', '4', '5', '6', '7+']" 
              class="mana-filter"
              :class="{'mana-filter-selected': filterMana[manaNr]}"
              @click="filterMana[manaNr] = !filterMana[manaNr]"
            >
              {{manaNr}}
            </div>

            <!-- Power Filter -->
            <div class="filter-title">
              Power
            </div>
            <div class="power-filter-container">
              <input type="number" v-model.number="filterPowerMin" placeholder="Min" class="power-filter" />
              <span>-</span>
              <input type="number" v-model.number="filterPowerMax" placeholder="Max" class="power-filter" />
            </div>

            <!-- Set Filter -->
            <div class="filter-title">
              Set
            </div>
            <div>
              <select 
                v-model="filterSet"
                class="catalogue-filter"
              >
                <option
                  class="set"
                  v-for="(set, index) in sets"
                  :key="index"
                  :value="set"
                  >{{ set }}</option
                >
              </select>
            </div>
            
            <div class="filter-title">
              Card Effect
            </div>
            <div>
              <input
                v-model="filterEffect"
                type="search"
                placeholder="Search cards by effect"
              />
            </div>

            <!-- Reset Filters Button -->
            <div>
              <img
                class="reset-icon"
                src="/assets/images/reset-icon.svg"
                v-tooltip="'Reset all filters'"
                @click="resetFilters"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sort Popup area -->
    <div v-if="showSortPopup" class="filter-popup-overlay">
      <div class="filter-popup">
        <button class="filter-close" @click="closeSort">
          ✕
        </button>

        <div class="filter-popup-content">
          <div class="filter-section">
            <div class="filter-title">
              Sort Options
            <div class="sort-options">
              <button class="filter-button" @click="sortCards('civilization')">Civilization</button>
              <button class="filter-button" @click="sortCards('type')">Type</button>
              <button class="filter-button" @click="sortCards('subtypes')">Race</button>
              <button class="filter-button" @click="sortCards('manaCost')">Cost</button>
              <button class="filter-button" @click="sortCards('power')">Power</button>
              <button class="filter-button" @click="sortCards('set')">Set</button>
              <button class="filter-button" @click="sortCards('name')">Name</button>
              <button class="filter-button" style="background: lightsalmon;" @click="resetSort()">Reset</button>
            </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { call } from "../remote";
import Header from "../components/Header.vue";
import VLazyImage from "v-lazy-image";

const ALL_FAMILIES = "All";
const ALL_SETS = "All Sets";

const CIV_ORDER = {
  light: 1,
  water: 2,
  darkness: 3,
  fire: 4,
  nature: 5,
};

const permissions = () => {
  let p = localStorage.getItem("permissions");
  if (!p) {
    return [];
  }
  return p;
};

function compareCards(card1, card2, sort) {
  var cat1 = card1[sort.by],
    cat2 = card2[sort.by];

  if (Array.isArray(cat1)) cat1 = cat1[0];
  if (Array.isArray(cat2)) cat2 = cat2[0];

  if (cat1 == null) cat1 = "";
  if (cat2 == null) cat2 = "";

  if (sort.by === "civilization") {
    const v1 = CIV_ORDER[cat1.toLowerCase()] || 99;
    const v2 = CIV_ORDER[cat2.toLowerCase()] || 99;

    if (v1 !== v2) {
      return sort.directionNum * (v1 - v2);
    }
  }

  return cat1 === parseInt(cat1, 10) && cat2 === parseInt(cat2, 10)
    ? sort.directionNum * (cat1 < cat2 ? -1 : cat1 > cat2 ? 1 : 0)
    : sort.directionNum * cat1.localeCompare(cat2);
}

function playSound(sound) {
  if (sound) {
    var audio = new Audio(sound);
    audio.volume = 0.2;
    audio.play();
  }
}

export default {
  name: "decks",

  components: {
    Header,
    VLazyImage,
  },

  computed: {
    username: () => localStorage.getItem("username"),
  },

  data() {
    return {
      warning: "",
      showWizard: false,

      filterCard: "",
      filterEffect: "",
      filterFamily: ALL_FAMILIES,
      filterSet: ALL_SETS,

      families: [ALL_FAMILIES, "Spell", "Creature"],

      filterCivilization: {
        light: false,
        water: false,
        darkness: false,
        fire: false,
        nature: false,
      },

      filterMana: {
        "1": false,
        "2": false,
        "3": false,
        "4": false,
        "5": false,
        "6": false,
        "7+": false,
      },

      filterPowerMin: null,
      filterPowerMax: null,

      sets: [],
      cards: [],
      decks: [],
      selectedCivilizations: [],

      selectedDeck: null,
      selectedDeckUid: null,
      deckCopy: null,

      previewCard: null,
      previewCardTop: 0,
      previewCardLeft: 0,
      previewCardWidth: 400,
      previewCardHeight: 560,

      cardSize: 360,

      draggedCard: null,
      dragOver: false,

      customOrderEnabled: false,
      draggedCardIndex: null,
      dragOverIndex: null,
      dropSide: null,

      dragSource: null, // "catalogue" | "builder"

      showFilterPopup: false,
      showSortPopup: false,
      currentSort: { by: null, directionNum: 1 },
    };
  },

  methods: {
    showPreview(card, event) {
      const normalWidth = 400;
      const normalHeight = 560;
      const scale = 1;

      let positionY = event.clientY - (normalHeight * scale) / 2;
      let positionX = event.clientX + 20;

      if (positionY + normalHeight * scale > window.innerHeight) {
        positionY = window.innerHeight - normalHeight * scale - 10;
      }

      if (positionY < 10) positionY = 10;

      if (positionX + normalWidth * scale > window.innerWidth) {
        positionX = window.innerWidth - normalWidth * scale - 10;
      }

      this.previewCardTop = positionY;
      this.previewCardLeft = positionX;
      this.previewCardWidth = normalWidth * scale;
      this.previewCardHeight = normalHeight * scale;
      this.previewCard = card;
    },

    hidePreview() {
      this.previewCard = null;
    },

    selectDeck(deck) {
      this.selectedDeck = deck;
      this.deckCopy = JSON.parse(JSON.stringify(deck));
    },

    cardInfo(uid) {
      let card = this.cards.find((x) => x.uid === uid);
      return card;
    },

    resetFilters() {
      Object.keys(this.filterCivilization).forEach(
        (civ) => (this.filterCivilization[civ] = false)
      );

      Object.keys(this.filterMana).forEach(
        (manaCost) => (this.filterMana[manaCost] = false)
      );

      this.filterFamily = ALL_FAMILIES;
      this.filterSet = ALL_SETS;
      this.filterCard = "";
      this.filterEffect = "";
      this.filterPowerMin = null;
      this.filterPowerMax = null;
      this.selectedCivilizations = [];
    },

    /*
    getCardsForDeck(cardUids) {
      let cards = [];

      for (let uid of cardUids) {
        let card = this.cards.find((x) => x.uid === uid);
        if (card === undefined) return [];

        card = JSON.parse(JSON.stringify(card));

        let existingCard = cards.find((x) => x.uid === card.uid);

        if (existingCard) {
          existingCard.count += 1;
        } else {
          card.count = 1;
          cards.push(card);
        }
      }
      
      cards.sort((c1, c2) =>
        compareCards(c1, c2, {
          by: "manaCost",
          directionNum: 1,
        })
      );

      return cards;
    },
    */

    getCardsForDeck(cardUids) {
      if (!this.selectedDeck) return [];

      let cards = [];

      for (let uid of cardUids) {
        let card = this.cards.find(x => x.uid === uid);
        if (!card) continue;

        cards.push({ ...card });
      }

      return cards;
    },

    tryAddCard(card) {
      const checkMaxDeckSize = this.selectedDeck.cards.length >= 40;
      const checkMaxCopies = this.selectedDeck.cards.filter((x) => x == card.uid).length >= 4;

      if (checkMaxDeckSize || checkMaxCopies) {
        playSound("/assets/sounds/card-limit.wav");
        return;
      }

      this.selectedDeck.cards.push(card.uid);
      playSound("/assets/sounds/card-added.mp3");
    },

    tryRemoveCard(card) {
      let uid = card.uid;
      let toSlice = this.selectedDeck.cards.indexOf(uid);

      if (toSlice < 0) return;

      playSound("/assets/sounds/card-removed.wav");
      this.selectedDeck.cards.splice(toSlice, 1);

      if (
        this.selectedDeck.cards.indexOf(uid) < 0 &&
        this.previewCard?.uid === uid
      ) {
        this.previewCard = null;
      }
    },

    onBuilderDragStart(index) {
      this.dragSource = "builder";
      this.draggedCardIndex = index;
    },

    onBuilderDragOver(index, event) {
      if (index === this.draggedCardIndex) return;

      const rect = event.currentTarget.getBoundingClientRect();
      const midpoint = rect.left + rect.width / 2;

      this.dragOverIndex = index;
      this.dropSide = event.clientX < midpoint ? "left" : "right";
    },

    onBuilderDrop(index) {
      if (!this.dragSource) return;

      let newIndex = index;
      if (this.dropSide === "right") newIndex++;

      if (this.dragSource === "builder") {
        const cards = this.selectedDeck.cards;
        const draggedCard = cards[this.draggedCardIndex];

        cards.splice(this.draggedCardIndex, 1);

        if (newIndex > this.draggedCardIndex) newIndex--;

        cards.splice(newIndex, 0, draggedCard);
      }

      if (this.dragSource === "catalogue") {
        // respect 40 card limit
        if (this.selectedDeck.cards.length >= 40) return;

        this.selectedDeck.cards.splice(newIndex, 0, this.draggedCard.uid);
      }

      // reset
      this.dragSource = null;
      this.draggedCardIndex = null;
      this.draggedCard = null;
      this.dragOverIndex = null;
      this.dropSide = null;
    },

    onBuilderDropEmpty(event) {
      // ignore if dropped on a card slot
      if (event.target.closest('.deck-card-slot')) return;
      if (this.dragSource !== "catalogue") return;
      if (this.selectedDeck.cards.length >= 40) return;

      this.selectedDeck.cards.push(this.draggedCard.uid);

      this.dragSource = null;
      this.draggedCard = null;
    },

    onCatalogueDragStart(card) {
      this.dragSource = "catalogue";
      this.draggedCard = card;
    },

    onDrop() {
      if (!this.draggedCard) return;

      this.tryAddCard(this.draggedCard);
      this.draggedCard = null;
    },

    toggleFilter() {
      this.showFilterPopup = true
    },

    closeFilter() {
      this.showFilterPopup = false
    },

    toggleSort() {
      this.showSortPopup = true
    },

    closeSort() {
      this.showSortPopup = false
    },

    resetSort() {
      this.currentSort = { by: null, directionNum: 1 };
    },

    sortCards(by) {
      if (this.currentSort.by === by) {
        this.currentSort.directionNum *= -1;
      } else {
        this.currentSort.by = by;
        this.currentSort.directionNum = 1;
      }
    },

    toggleCivilization(civ) {
      // Toggle the filter state for card filtering
      this.filterCivilization[civ] = !this.filterCivilization[civ];

      // Update selectedCivilizations for the UI border to match the filter state
      const index = this.selectedCivilizations.indexOf(civ);
      if (this.filterCivilization[civ]) { // If it is now selected for filtering
        if (index === -1) { // And it's not already in the UI selection list
          this.selectedCivilizations.push(civ); // Add it to the UI selection list
        }
      } else { // If it is now deselected for filtering
        if (index !== -1) { // And it is currently in the UI selection list
          this.selectedCivilizations.splice(index, 1); // Remove it from the UI selection list
        }
      }
    },

    modifyCatalogueCardSize(addition) {
      this.cardSize += addition;
    },

    copyDeckList() {
      const cards = this.getCardsForDeck(this.selectedDeck.cards);

      const deckList = cards.map(
        (card) => `${card.count}x ${card.name}`
      );

      this.warning = `${deckList.join("\n")}

      Total Cards: ${this.selectedDeck.cards.length}`;
    },

    newDeck() {
      if (!this.decksEqual(this.selectedDeck, this.deckCopy)) {
        this.warning =
          "Please save or discard the changes you've made before creating a new deck";
        return;
      }

      this.decks.push({
        name: "Unnamed Deck",
        cards: [],
        public: false,
      });

      this.deckCopy = JSON.parse(
        JSON.stringify(this.decks[this.decks.length - 1])
      );

      this.selectedDeck = this.decks[this.decks.length - 1];
      this.selectedDeckUid = this.selectedDeck.uid;

      this.$nextTick(() => {
        this.deckCopy.name = "to.be.removed";
      });
    },

    closeOverlay() {
      this.warning = null;
    },

    async save() {
      try {
        await call({
          path: "/decks",
          method: "POST",
          body: this.selectedDeck,
        });

        this.deckCopy = JSON.parse(
          JSON.stringify(this.selectedDeck)
        );

        this.warning = "Successfully saved your deck";
      } catch (e) {
        this.warning =
          "Invalid request. Please ensure that the deck name is 1-30 characters and that you have between 40-50 cards in your deck.";
      }
    },

    async deleteDeck() {
      try {
        await call({
          path: "/deck/" + this.selectedDeckUid,
          method: "DELETE",
        });

        this.decks = this.decks.filter(
          (x) => x.uid !== this.selectedDeckUid
        );

        if (this.decks.length > 0) {
          this.selectedDeckUid = this.decks[0].uid;
          this.selectDeck(this.decks[0]);
        } else {
          this.newDeck();
        }

        this.warning = "Successfully deleted your deck";
      } catch (e) {
        this.warning = "Couldn't delete the deck you selected";
      }
    },

    discard() {
      if (this.deckCopy.name === "to.be.removed") {
        this.selectedDeck = this.decks[0];
        this.deckCopy = JSON.parse(
          JSON.stringify(this.selectedDeck)
        );
        this.selectedDeckUid = this.selectedDeck.uid;
        this.decks.pop();
        return;
      }

      this.selectedDeck = JSON.parse(
        JSON.stringify(this.deckCopy)
      );
    },

    decksEqual(deck1, deck2) {
      if (deck1.name !== deck2.name) return false;
      if (deck1.public !== deck2.public) return false;
      if (deck1.cards.length !== deck2.cards.length) return false;

      for (let i = 0; i < deck1.cards.length; i++) {
        if (deck1.cards[i] !== deck2.cards[i]) return false;
      }

      return true;
    },
    
    /*
    displayFamily(family) {
      return family ? family.join(" / ") : "Spell";
    },
    */
  },

  async created() {
    try {
      let [cards, decks] = await Promise.all([
        call({ path: "/cards", method: "GET" }),
        call({ path: "/decks", method: "GET" }),
      ]);

      let sets = {};
      let cardsCiv = {
        light: [],
        water: [],
        darkness: [],
        fire: [],
        nature: [],
      };

      for (let card of cards.data) {
        cardsCiv[card.civilization.toLowerCase()].push(card);

        if (!sets[card.set]) {
          sets[card.set] = true;
        }
      }

      this.sets = Object.keys(sets);
      this.sets.push(ALL_SETS);
      this.sets.sort();

      let sortedCards = [];

      Object.values(cardsCiv).forEach((civSet) =>
        sortedCards.push(
          ...civSet.sort((c1, c2) =>
            compareCards(c1, c2, {
              by: "manaCost",
              directionNum: 1,
            })
          )
        )
      );

      this.cards = sortedCards;
      this.decks = decks.data;

      if (this.decks.length < 1) {
        this.decks.push({
          name: "My first deck",
          cards: [],
          public: false,
        });
      }

      let families = [];

      for (let c of this.cards) {
        if (c.family) {
          for (let f of c.family) {
            if (!families.includes(f)) {
              families.push(f);
            }
          }
        }
      }

      families.sort();
      this.families.push(...families);

      this.selectedDeck = this.decks[0];
      this.deckCopy = JSON.parse(
        JSON.stringify(this.selectedDeck)
      );
      this.selectedDeckUid = this.selectedDeck.uid;
    } catch (e) {
      console.log(e);
    }
  },

  watch: {
    selectedDeckUid(val) {
      if (!this.decksEqual(this.selectedDeck, this.deckCopy)) {
        this.warning =
          "You have unsaved changes in the currently selected deck. Save or discard before editing another deck.";
        this.selectedDeckUid = this.selectedDeck.uid;
        return;
      }

      this.selectedDeck = this.decks.find((x) => x.uid === val);
      this.deckCopy = JSON.parse(
        JSON.stringify(this.selectedDeck)
      );
    },
  },

  computed: {
    filteredAndSortedCards() {
      let cards = this.cards.filter(
        (card) =>
          card.name
            .toLowerCase()
            .includes(this.filterCard.toLowerCase()) &&
          (this.filterEffect === "" ||
            card.text
              .toLowerCase()
              .includes(this.filterEffect.toLowerCase()))
      );

      if (this.filterSet !== ALL_SETS) {
        cards = cards.filter(
          (card) => card.set === this.filterSet
        );
      }

      let filterCivilizationValues =
        Object.values(this.filterCivilization);

      if (
        !filterCivilizationValues.every(
          (v) => v === filterCivilizationValues[0]
        )
      ) {
        cards = cards.filter(
          (card) =>
            this.filterCivilization[card.civilization]
        );
      }

      if (
        this.filterFamily.toLowerCase() !==
        ALL_FAMILIES.toLowerCase()
      ) {
        cards = cards.filter(
          (card) =>
            (this.filterFamily.toLowerCase() === "spell" &&
              !card.family) ||
            (this.filterFamily.toLowerCase() === "creature" &&
              card.family) ||
            (card.family &&
              card.family.includes(this.filterFamily))
        );
      }

      let filterManaValues = Object.values(this.filterMana);

      if (
        !filterManaValues.every(
          (v) => v === filterManaValues[0]
        )
      ) {
        cards = cards.filter((card) => {
          if (card.manaCost > 6)
            return this.filterMana["7+"];
          else
            return this.filterMana[
              card.manaCost.toString()
            ];
        });
      }

      if (this.filterPowerMin != null || this.filterPowerMax != null) {
        cards = cards.filter((card) => {
          const power = parseInt(card.power, 10);

          if (isNaN(power)) return false; // Cards with no power should be ignored (e.g. spells)
          if (this.filterPowerMin != null && power < this.filterPowerMin) return false;
          if (this.filterPowerMax != null && power > this.filterPowerMax) return false;

          return true;
        });
      }

      if (this.currentSort.by) {
        cards.sort((c1, c2) => compareCards(c1, c2, this.currentSort));
      }

      return cards;
    },
  },
};
</script>

<style scoped>
/* Main layout */
.main {
  display: flex;
  flex-direction: column;
  height: 100%
}


/* Deck building area */
.deck-panel {
  display: grid;
  height: 60%;
  width: 32%;
  grid-template-columns: repeat(8, 1fr);
  grid-template-rows: repeat(5, 1fr);
  column-gap: 3px;
  row-gap: 0px;
  margin: 0 auto;
}

.deck-card-slot.dragging {
  opacity: 0.5;
  transform: scale(1.05);
}

.deck-card-slot.drop-left {
  border-left: 4px solid #ff9800;
}

.deck-card-slot.drop-right {
  border-right: 4px solid #ff9800;
}

.deck-card-slot img {
  height: 100%;
  width: 100%;
  object-fit: contain;
  border-radius: 3px;
}


/* Card catalogue area */
.catalogue-cards-wrapper {
  height: 20%;
  overflow-x: auto;
  overflow-y: hidden;
}

.catalogue-cards {
  height: 100%;
  display: flex;
  flex-wrap: nowrap;
  column-gap: 8px;
}

.catalogue-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.catalogue-card:hover {
  transform: scale(1.05);
}

.catalogue-card img {
  height: 21vh;
  width: 7vw;
  object-fit: contain;
  border-radius: 4px;
}


/* Card search input area */
.catalogue-search {
  height: 5%;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.catalogue-search input {
  flex: 1;
}


/* filter button area */
.filter-button {
  padding: 4px 12px;
  border-radius: 6px;
  border: none;
  background: #444;
  color: white;
  cursor: pointer;
  transition: background 0.15s ease;
}

.filter-button:hover {
  background: #666;
}


/* filter popup box area */
.filter-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.filter-popup {
  position: relative;
  background: #1e1e1e;
  color: white;
  padding: 16px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}

.filter-close {
  position: absolute;
  top: 8px;
  right: 8px;
  border: none;
  background: transparent;
  color: white;
  font-size: 18px;
  cursor: pointer;
}

.filter-close:hover {
  opacity: 0.7;
}

.filter-popup-content {
  margin-top: 10px;
}

.filter-section {
  margin-bottom: 12px;
}

.filter-title {
  font-weight: bold;
  margin-bottom: 6px;
}


/* Civilization filter buttons */
.civ-icons {
  display: flex;
  gap: 8px;
}

.civ-filter {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: inline-block;
  cursor: pointer;
  border: 4px solid #e0dede;
  /*transition: 0.15s ease;*/
  margin-left: 5px;
}

.civ-filter-selected {
  border: 4px solid black;
}

/*
.civ-filter:hover {
  transform: scale(1.1);
}*/

.civ-color-fire {
  background-color: #D12027;
}

.civ-color-water {
  background-color: #47C6F2;
}

.civ-color-light {
  background-color: #FAD241;
}

.civ-color-darkness {
  background-color: #65696C;
}

.civ-color-nature {
  background-color: #118141;
}


/* Type and set filter dropdown */
.catalogue-filter {
  background-color: black;
  color: white;
}

/* Sort button area */
.sort-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}


/* Mana filter buttons */
.mana-filter {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-left: 5px;
  cursor: pointer;
  color: white  ;
  background-color: black;
  font-weight: 600;
  border: 4px solid #e0dede;
}

.mana-filter-selected {
  border: 4px solid orange;
}


/* Reset filters button */
.reset-icon {
  width: 35px;
  /*margin-left: 20px;*/
  background-color: lightsalmon;
  cursor: pointer;
}


/* Card preview on hover */
.card-preview {
  position: fixed;           /* independent of parent grid/flex */
  z-index: 1000;             /* always on top */
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0,0,0,0.5);
  pointer-events: none;      /* lets the cursor pass through */
  transition: transform 0.2s ease, width 0.2s ease, height 0.2s ease;
}

.card-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}
</style>