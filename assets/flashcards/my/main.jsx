import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import '../../static/main.scss'

const app = ReactDOM.createRoot(document.getElementById('app'));

app.render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>
)
