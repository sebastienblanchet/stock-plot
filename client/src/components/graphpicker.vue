<template>
  <v-card class="mx-5 my-5">
    <v-card-text>
      <v-row>
        <v-card elevation="0" class="mx-5">
          <!-- returns object -->
          <v-select
            v-model="selected"
            item-text="name"
            item-value="id"
            label="Display"
            :items="getPlots"
          ></v-select>
        </v-card>
      </v-row>
      <v-row>
        <v-col cols="12">
          <generic v-if="selected.length > 0" :propId="selected" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import gql from "graphql-tag";
import generic from "./generic.vue";

export default {
  name: "picker",
  components: {
    // editor
    generic
  },
  data: () => ({
    getPlots: null,
    selected: ""
  }),
  apollo: {
    getPlots: gql`
      {
        getPlots {
          id
          name
        }
      }
    `
  },
  created() {
    // TODO fix this cheat
    this.selected = this.getPlots ? this.getPlots[0].id : "abc";
  }
};
</script>

<style>
.layout .jsoneditor-vue {
  height: 150px;
}

.data .jsoneditor-vue {
  height: 300px;
}

.jsoneditor-vue div.jsoneditor-tree {
  min-height: 100px;
}

.mark-up {
  margin-top: 8px;
}

.graph {
  height: 500px;
}

div.jsoneditor-menu {
  background-color: #007bff;
  border-bottom: 1px solid #007bff;
}

.descriptor > span {
  margin-left: 5px;
  margin-top: 5px;
}
</style>
