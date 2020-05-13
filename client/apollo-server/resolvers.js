import GraphQLJSON from 'graphql-type-json'

function getUrl(ticker, interval)
return `https: //www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${ticker}&interval=${interval}&apikey=${process.env.ALPHA_API_KEY}`
}

export default {
  JSON: GraphQLJSON,
  Query: {
    getPlots: (root, {}) => {
      return {};
    },
    getPlotly: (root, {
      ticker,
      interval
    }) => {
      let url = getUrl(ticker, interval);
      console.log(url);
      return url;
    }
  },
  Mutation: {
    myMutation: (root, args, context) => {
      const message = 'My mutation completed!'
      context.pubsub.publish('hey', {
        mySub: message
      })
      return message
    },

  }
}