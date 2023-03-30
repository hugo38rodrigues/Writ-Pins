import React, { useState, useEffect } from "react";
import axios from "axios";

const User = () => {
    const [users, setUsers] = useState([]);
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [mdp, setMdp] = useState("");
    const [selectedUser, setSelectedUser] = useState(null);

    useEffect(() => {
        getUsers();
    }, []);

    const getUsers = async () => {
        const response = await axios.get("http://localhost:5000/users");
        setUsers(response.data);
    };

    const createUser = async () => {
        await axios.post("http://localhost:5000/v0/post/users", { name, email });
        setName("");
        setEmail("");
        setMdp("");
        getUsers();
    };

    const updateUser = async () => {
        await axios.put(`http://localhost:5000/v0/put/user/${selectedUser._id}`, {
            name,
            email,
        });
        setName("");
        setEmail("");
        setSelectedUser(null);
        getUsers();
    };

    const deleteUser = async (id) => {
        await axios.delete(`http://localhost:5000/v0/delete/users/${id}`);
        getUsers();
    };

    const selectUser = (user) => {
        setSelectedUser(user);
        setName(user.name);
        setEmail(user.email);
    };

    return (
        <div>
            <h1>User</h1>
            <form onSubmit={selectedUser ? updateUser : createUser}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="mdp"
                    placeholder="mot de passe"
                    value={mdp}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <button type="submit">{selectedUser ? "Update" : "Create"}</button>
            </form>
            <ul>
                {users.map((user) => (
                    <li key={user._id}>
                        {user.name} - {user.email}
                        <button onClick={() => selectUser(user)}>Edit</button>
                        <button onClick={() => deleteUser(user._id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default User;
