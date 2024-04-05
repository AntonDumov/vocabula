import Decks from "./Components/Decks.jsx";
import {ProfileProvider} from "./ProfileContext.jsx";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import NavBar from "./Components/NavBar.jsx";
import Deck from "./Components/Deck.jsx";
import Home from "./Components/Home.jsx";

function App() {
    return (
        <ProfileProvider>
            <NavBar/>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/flashcards/" element={<Decks/>}/>
                    <Route path="/flashcards/:id/" element={<Deck/>}/>
                </Routes>
            </BrowserRouter>

        </ProfileProvider>
    )
}

export default App
