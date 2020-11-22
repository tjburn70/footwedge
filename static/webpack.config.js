const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path')

const config = {
    entry: __dirname + '/src/index.js',
    output: {
        path: path.join(__dirname, '/dist'),
        publicPath: '/dist/',
        filename: 'bundle.js'
    },
    resolve: {
        alias: {
            src: path.resolve(__dirname, './src')
        },
        extensions: ['.js', '.jsx']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            }
        ]
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: path.join(__dirname, '/public/index.html'),
            filename: "index.html",
            inject: "body",
        })
    ],
    devServer: {
        contentBase: path.join(__dirname, '/public'),
    },
};

module.exports = config;