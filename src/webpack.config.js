const path = require('path');

module.exports = {
  watch: true,
  entry: './client/static/client.js',
  output: {
    path: path.resolve(__dirname, 'server/dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
    ],
  },
};