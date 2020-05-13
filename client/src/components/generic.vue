<template>
  <div v-if="getPlotly != null">
    <v-row align="center">
      <v-col cols="4">
        <v-card elevation="0" class="mx-5">
          <v-card-title>Layout</v-card-title>
          <editor
            class="editor"
            v-model="getPlotly.layout"
            :show-btns="false"
          />
        </v-card>
        <v-card elevation="0" class="mx-5">
          <v-card-title>Data</v-card-title>
          <editor class="editor" v-model="getPlotly.data" :show-btns="false" />
        </v-card>
        <v-card elevation="0" class="mx-5">
          <v-card-title>Attributes</v-card-title>
          <editor class="editor" v-model="getPlotly.attr" :show-btns="false" />
        </v-card>
      </v-col>
      <v-col cols="8 text--center">
        <v-card>
          <plotly
            v-bind="getPlotly.attr"
            :data="getPlotly.data"
            :layout="getPlotly.layout"
          />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import gql from "graphql-tag";
import editor from "vue-json-editor";

export default {
  name: "generic",
  components: {
    editor
  },
  props: {
    propId: String
  },
  data: () => ({
    getPlotly: null
  }),
  apollo: {
    // Simple query that takes in prop with
    // must have same name as query
    getPlotly: {
      query: gql`
        query GetPlotly($id: ID!) {
          getPlotly(id: $id) {
            id
            data {
              type
              x
              y
              z
            }
            layout {
              title
              paper_bgcolor
            }
            attr {
              displayModeBar
            }
          }
        }
      `,
      variables() {
        // Use vue reactive properties here
        return {
          id: this.propId
        };
      }
    }
  },
  computed: {},
  methods: {
    vector2Matrix(data) {
      var cpy = data.z;
      var z = [];

      const c = data.x.length;
      const r = data.y.length;

      // check that square matrix provided
      if (c == r) {
        while (cpy.length) {
          z.push(cpy.splice(0, c));
        }
      }
      data.z = z;
      return data;
    }
  },
  watch: {
    getPlotly() {
      // unpack z data
      if (this.getPlotly.data) {
        this.getPlotly.data.forEach(element => {
          // check that the z data has not been processed yet
          if (element.z && !element.z[0].length) {
            var dimensions = [element.z.length, element.z[0].length];
            console.log(dimensions);
            element = this.vector2Matrix(element);
          }
        });
      }
    }
  }
};
</script>

<style scoped>
.editor {
  max-width: %100;
}
</style>
