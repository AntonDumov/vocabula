import {useEffect, useRef, useState} from "react";
import axiosInstance from "../../../axiosInstance.js";
import djangoReverse from "../../../djangoReverse.js";
import {useParams} from "react-router-dom";

const urls = await djangoReverse();

const Deck = () => {
    const {id} = useParams();
    const deckId = parseInt(id);
    const [deck, setDeck] = useState(null)
    const [flashcards, setFlashcards] = useState([])

    const newFlashcardQuestion = useRef(null);
    const newFlashcardAnswer = useRef(null);

    useEffect(() => {
        fetchDeckData().then(
            (deck) => {
                fetchFlashcards(deck.id);
            }
        );
    }, []);

    const fetchDeckData = async () => {
        try {
            const r = await axiosInstance(
                urls['flashcards:deck-detail']({pk: deckId})
            );
            setDeck(r.data)
            return r.data
        } catch (e) {
            console.log(`Failed to fetch deck: ${e.message}`);
        }
    }

    const fetchFlashcards = async (deckId = null) => {
        try {
            const response = await axiosInstance(
                urls['flashcards:deck-flashcards-list']({deck_pk: deckId ? deckId : deck.id})
            );
            setFlashcards(response.data)
        } catch (e) {
            console.log(`Failed to fetch flashcards: ${e.message}`);
        }
    }

    const addFlashcard = async (question, answer) => {
        try {
            const r = await axiosInstance(
                urls['flashcards:deck-flashcards-list']({deck_pk: deck.id}), {
                    method: 'POST',
                    data: {question, answer}
                }
            )
            setFlashcards([...flashcards, r.data])
        } catch (e) {
            console.log(`Failed to add flashcard: ${e.message}`);
        }
    }

    const handleAddFlashcard = () => {
        addFlashcard(newFlashcardQuestion.current.value, newFlashcardAnswer.current.value);
        newFlashcardQuestion.current.value = '';
        newFlashcardAnswer.current.value = '';
    }

    return (<div>
            {deck ? (
                <div>
                    <h2>Deck: {deck.name}</h2>
                    <p>{deck.description}</p>
                </div>
            ) : ''}
            <input type='text' placeholder='Flashcard Question' ref={newFlashcardQuestion}/>
            <input type='text' placeholder='Flashcard Answer' ref={newFlashcardAnswer}/>
            <button type='button' className="btn btn-primary" onClick={() => handleAddFlashcard()}
            >Add Flashcard
            </button>
            {
                flashcards ? (
                    <div className="table-responsive">
                        <table className="table table-striped">
                            <tbody>
                            {flashcards.map((f) => (
                                <tr key={f.id}>
                                    <td>{f.question}</td>
                                    <td>{f.answer}</td>
                                </tr>
                            ))}
                            </tbody>
                        </table>
                    </div>
                ) : ''
            }
        </div>
    )
}

export default Deck;