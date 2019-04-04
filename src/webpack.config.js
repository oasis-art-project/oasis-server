const webpack = require('webpack');
const resolve = require('path').resolve;

const config = {
        devtool: 'eval-source-map',
 	entry: __dirname + '/static/js/index.jsx',
 	output:{
      path: resolve('public/'),
      filename: 'bundle.js',
			publicPath: ('public/')
 	},
 	resolve: {
  	extensions: ['.js','.jsx','.css']
 	},
 	module: {
  	rules: [
		{
  		test: /\.jsx?/,
   		loader: 'babel-loader',
  		exclude: /node_modules/,
   		query:{
     		presets: ['@babel/react','@babel/env']
   		}
  	},
		{
  		test: /\.css$/,
    	loader: 'style-loader!css-loader?modules'
  	},
		{
    	test: /\.(png|jpg|gif)$/,
    	use: [{
            loader: 'file-loader',
            options: {},
          }],
		}]
 	}
};
module.exports = config;
