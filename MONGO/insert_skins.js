// Connect to the MongoDB server
var conn = new Mongo();
var db = conn.getDB("J2D"); // Change to your database name

// Skins data to be inserted
var skinsToInsert = [
    {
        name: "Nebula Fury",
        price: 25.99,
        color: "Purple",
        rarity: "Rare"
    },
    {
        name: "Shadow Walker",
        price: 19.50,
        color: "Black",
        rarity: "Common"
    },
    {
        name: "Chrono Pulse",
        price: 30.75,
        color: "Gold",
        rarity: "Epic"
    },
    {
        name: "Celestial Haze",
        price: 15.99,
        color: "Blue",
        rarity: "Uncommon"
    },
    {
        name: "Phoenix Ember",
        price: 22.49,
        color: "Red",
        rarity: "Legendary"
    }
];

// Insert skins into the "skins" collection
db.skins.insertMany(skinsToInsert);
