import {createContext, useCallback, useContext, useEffect, useState} from "react";
import djangoReverse from "../../djangoReverse.js";
import axiosInstance from "../../axiosInstance.js";


const urls = await djangoReverse();

export const ProfileContext = createContext({});

export const ProfileProvider = (props) => {
    const [profile, setProfile] = useState({})

    const fetchProfile = useCallback(async () => {
        try {
            const r = await axiosInstance(urls['flashcards:my-profile']())
            setProfile(r.data)
        } catch (e) {
            console.log(`Failed to fetch profile: ${e.message}`)
        }
    }, [])

    useEffect(() => {
        fetchProfile()
    }, []);

    return (
        <ProfileContext.Provider value={{profile}}>
            {props.children}
        </ProfileContext.Provider>
    )
}

export const useProfileContext = () => useContext(ProfileContext);
