// Connect to the MongoDB server
var conn = new Mongo();
var db = conn.getDB("J2D"); // Change to your database name

// Users data to be inserted
var usersToInsert = [
    {
        id: 1,
        username: "user1",
        email: "user1@example.com",
        password: "password1",
        balance: 100.00,
        owned_skins: [
            { id: 1, color: "Red" },
            { id: 3, color: "Green" }
        ]
    },
    {
        id: 2,
        username: "user2",
        email: "user2@example.com",
        password: "password2",
        balance: 50.50,
        owned_skins: [
            { id: 2, color: "Blue" },
            { id: 4, color: "Purple" }
        ]
    },
    {
        id: 3,
        username: "user3",
        email: "user3@example.com",
        password: "password3",
        balance: 75.25,
        owned_skins: [
            { id: 1, color: "Red" },
            { id: 5, color: "Gold" }
        ]
    }
];

// Insert users into the "users" collection
db.users.insertMany(usersToInsert);

// Output the result
print("Users inserted successfully!");
