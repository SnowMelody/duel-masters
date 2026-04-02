<template>
  <div>
    <span class="title">Welcome, {{ username }}!</span>
    <nav>
      <ul>
        <li @click="$router.push('overview')" class="">Lobby</li>
        <li class="no-cursor">|</li>
        <li @click="$router.push('decks')">Decks</li>
      </ul>
    </nav>
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";

export default {
  name: "decks",
  computed: {
    username: () => localStorage.getItem("username"),
    changelog() {
      return marked.parse(this.rawChangelog);
    }
  },
  data() {
    return {
      changelogOpen: false,
      changelogLastClosed: 0,
      rawChangelog:
        "Failed to load changelog.. Please refresh the site and try again"
    };
  },
  created() {
    axios
      .get(
        "https://raw.githubusercontent.com/sindreslungaard/duel-masters/master/CHANGELOG.md"
      )
      .then(res => {
        this.rawChangelog = res.data;
      });
  },
  methods: {
    toggleChangelog() {
      if (!this.changelogOpen) {
        if (this.changelogLastClosed > Date.now() - 300) {
          return;
        }
        this.changelogOpen = true;
        this.$nextTick(() => {
          this.$refs.changelogpopup.focus();
        });
      } else {
        this.closeChangelog();
      }
    },
    closeChangelog() {
      this.changelogOpen = false;
      this.changelogLastClosed = Date.now();
    }
  }
};
</script>

<style scoped>
.main {
  margin: 0 15px;
}

.new-duel .backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: #000;
  opacity: 0.5;
}

.new-duel .wizard {
  position: absolute;
  top: calc(50vh - 323px / 2);
  left: calc(50% - 250px / 2);
  background: #36393f;
  width: 250px;
  border-radius: 4px;
  color: #fff;
  border: 1px solid #666;
}

.wizard .headline {
  color: #ccc;
}

.wizard .spacer {
  margin: 15px;
}

.wizard .helper {
  color: #ccc;
  font-size: 13px;
}

.wizard .btn {
  margin: 0;
  width: 85px;
  text-align: center;
  margin-top: 15px;
}

.wizard .cancel {
  margin-left: 10px;
  background: #ff4c4c;
  color: #fff;
}

.wizard .cancel:hover {
  background: #ed3e3e;
}

input,
textarea,
select {
  border: none;
  background: #484c52;
  padding: 10px;
  border-radius: 4px;
  width: 200px;
  color: #ccc;
  resize: none;
}
input:focus,
textarea:focus,
select:focus {
  outline: none;
}
input:active,
textarea:active,
select:active {
  outline: none;
}

.wizard select {
  width: 220px;
  margin-top: 4px;
}

.wizard .errorMsg {
  color: red;
  font-size: 14px;
  display: block;
  margin-top: 15px;
}

nav {
  text-align: right;
}

ul {
  list-style: none;
}

li {
  display: inline-block;
  padding-right: 10px;
  margin-right: 10px;
}

nav > ul > li:hover {
  cursor: pointer;
  color: #fff;
}

nav > ul > li.no-cursor:hover {
  cursor: default;
}

.title {
  position: absolute;
  top: 16px;
  left: 16px;
}

.psa {
  margin: 16px;
  background: url(/assets/images/overlay_30.png);
  padding: 5px;
  min-height: 20px;
  border-radius: 4px;
  font-size: 14px;
  color: #ccc;
}

.psa > span {
  display: inline-block;
  vertical-align: middle;
  margin-left: 4px;
}

a {
  color: #7289da;
}

.btn {
  display: inline-block;
  background: #7289da;
  color: #e3e3e5;
  font-size: 14px;
  line-height: 20px;
  padding: 5px 10px;
  border-radius: 4px;
  transition: 0.1s;
  text-align: center !important;
  user-select: none;
}

.btn:hover {
  cursor: pointer;
  background: #677bc4;
}

.btn:active {
  background: #5b6eae !important;
}

.patreon-btn {
  width: 125px;
  margin-bottom: -10px;
  border-radius: 4px;
  margin-right: -3px;
  opacity: 0.9;
}

.patreon-btn:hover {
  opacity: 1;
}

.github-icon {
  margin-bottom: -8px;
  opacity: 0.8;
}

.github-icon:hover {
  opacity: 0.9;
}

.changelog {
  position: relative;
}

.changelog-popup {
  position: absolute;
  top: 33px;
  right: 0;
  width: 400px;
  height: 500px;
  background: #0A0A0D;
  border-radius: 4px;
  text-align: left;
  cursor: default;
  z-index: 200;
  outline: none;
}

.changelog-popup:after {
  content: "";
  width: 15px;
  height: 15px;
  top: -3px;
  right: 10px;
  transform: rotate(45deg);
  background: #0A0A0D;
  position: absolute;
  z-index: 998;
}

.changelog-md {
  font-size: 11px;
  padding: 0 20px;
  overflow-y: scroll;
  height: 500px;
}

*::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px #222;
  box-shadow: inset 0 0 6px #222;
  background-color: #484c52;
}

*::-webkit-scrollbar {
  width: 6px;
  height: 6px;
  background-color: #484c52;
}

*::-webkit-scrollbar-thumb {
  -webkit-box-shadow: inset 0 0 6px #222;
  box-shadow: inset 0 0 6px #222;
  background-color: #222;
}
</style>