import React, {useState, useEffect} from "react";
import axios from "axios";

const Pins = () => {
    const [pins, setPins] = useState([]);
    const [titre, setTitre] = useState([]);
    const [description, setDescription] = useState("");
    const [tags, setTags] = useState("");
    const [status, setStatus] = useState("");
    const [selectedPins, setSelectedPins] = useState(null);

    useEffect(() => {
        getPins();
    }, []);

    const getPins = async () => {
        const response = await axios.get("http://localhost:5000/v0/get/users");
        setPins(response.data);
    };

    const createPins = async () => {
        await axios.post("http://localhost:5000/v0/post/users", {
            titre: titre,
            description: description,
            tags: tags,
            status: status
        });
        setTitre("");
        setDescription("");
        setTags("");
        setStatus("");
        getPins();
    };

    const updatePins = async () => {
        await axios.put(`http://localhost:5000/v0/put/users/${selectedPins._id}`, {
            titre: titre,
            description: description,
            tags: tags,
            status: status
        });
        setDescription("");
        setTags("");
        setStatus("");
        setDescription("");
        setTitre()
        setSelectedPins(null);
        getPins();
    };

    const deletePins = async (id) => {
        await axios.delete(`http://localhost:5000/v0/delete/pins/${id}`);
        getPins();
    };

    const selectPins = (pin) => {
        setSelectedPins(pin);
        setDescription(pin.description);
        setTags(pin.tags);
        setTitre(pin.titre);
        setStatus(pin.status);
    };

    return (
        <div>
            <h1>Pins</h1>
            <form onSubmit={selectedPins ? updatePins : createPins}>
                <input
                    type="titre"
                    placeholder="titre"
                    value={titre}
                    onChange={(e) => setTitre(e.target.value)}
                />
                <input
                    type="description"
                    placeholder="descritpion"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <input
                    type="tags"
                    placeholder="tags"
                    value={tags}
                    onChange={(e) => setTags(e.target.value)}
                />
                <select name="pets" id="pet-select">
                    <option value="">-Choisisez une option</option>
                    <option value="1">Public</option>
                    <option value="0">Privé</option>
                </select>
                <button type="submit">{selectedPins ? "Update" : "Create"}</button>
            </form>
            <ul>
                {pins.map((pin) => (
                    <li key={pin._id}>
                        {pin.title}
                        {pin.description}
                        {pin.status}
                        {pin.tags}
                        <button onClick={() => selectPins(pin)}>Edit</button>
                        <button onClick={() => deletePins(pin._id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Pins;
