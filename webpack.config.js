import path from 'path';


export default {
    devtool: 'source-map',
    entry: {
        my: './assets/flashcards/my/main.jsx',
    },  // path to our input file
    output: {
        filename: '[name].bundle.js',  // output bundle file name
        path: path.resolve(process.env.PWD, './compiled'),  // path to our Django static directory
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: {presets: ["@babel/preset-env", ["@babel/preset-react", {"runtime": "automatic"}]]}
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                    "style-loader",
                    "css-loader",
                    {
                        loader: 'postcss-loader',
                        options: {
                            postcssOptions: {
                                plugins: [
                                    'autoprefixer'
                                ]
                            }
                        }
                    },
                    "sass-loader",
                ],
            },
        ]
    },
    watch: true,
};