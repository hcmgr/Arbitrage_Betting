const path = require('path');

module.exports = {
    entry: './src/client/static/index.js',
    output: {
      path: path.resolve(__dirname, '../src/server/bundles'),
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