const path = require('path');

module.exports = {
    entry: './client/static/index.js',
    output: {
      path: path.resolve(__dirname, 'server/dist'),
      filename: 'bundle.js',
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
          },
        },
      ],
    },
    resolve: {
      extensions: ['.js', '.jsx'],
    },
  };