import {useProfileContext} from "../ProfileContext.jsx";
import djangoReverse from "../../../djangoReverse.js";
import axiosInstance from "../../../axiosInstance.js";
import {useEffect, useState} from "react";

const urls = await djangoReverse();

const Decks = (props) => {
    const [decks, setDecks] = useState([]);
    const [newDeckName, setNewDeckName] = useState('');
    const [newDeckDescription, setNewDeckDescription] = useState('');

    const {profile} = useProfileContext()

    useEffect(() => {
        fetchDecks()
    }, []);

    const fetchDecks = async () => {
        try {
            const r = await axiosInstance(urls['flashcards:deck-list']());
            setDecks(r.data);
        } catch (e) {
            console.log(`Failed to fetch decks: ${e.message}`);
        }
    }

    const handleAddDeck = async () => {
        const newDeck = {
            name: newDeckName,
            description: newDeckDescription
        };
        try {
            const r = await axiosInstance(urls['flashcards:deck-list'](), {
                method: 'POST',
                data: newDeck
            });
            setDecks([...decks, r.data]);
        } catch (e) {
            console.log(`Failed to add deck: ${e.message}`);
        }
    };
    const handleDeleteDeck = async (deckId) => {
        try {
            const r = await axiosInstance(urls['flashcards:deck-detail']({pk:deckId}), {
                method: 'DELETE',
            })
            setDecks(decks.filter((deck) => deck.id !== deckId));
        } catch (e) {
            console.log(`Failed to delete deck: ${e.message}`);
        }
    }

    return (
        <div>
            <input type="text" placeholder="Deck name" value={newDeckName}
                   onChange={(e) => setNewDeckName(e.target.value)}/>
            <input type="text" placeholder="Deck description" value={newDeckDescription}
                   onChange={(e) => setNewDeckDescription(e.target.value)}/>
            <button onClick={handleAddDeck}>Add new deck</button>
            {decks ? (
                <div className='table-responsive'>
                    <table className='table table-striped'>
                        <tbody>
                        {decks.map((deck, index) => (
                            <tr key={deck.id}>
                                <td><a
                                    href={`/flashcards/${deck.id}`}>{deck.name}</a>
                                </td>
                                <td>{deck.description}</td>
                                <td>
                                    <button type='button' onClick={() => handleDeleteDeck(deck.id)}>Delete Deck</button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            ) : ''
            }
        </div>
    );
};

export default Decks