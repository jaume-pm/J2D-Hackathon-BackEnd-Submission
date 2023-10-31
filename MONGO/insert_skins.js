// Connect to the MongoDB server
var conn = new Mongo();
var db = conn.getDB("J2D"); // Change to your database name

// Skins data to be inserted
var skinsToInsert = [
    {
        name: "Skin A",
        price: 25.99,
        color: "Red",
        rarity: "Rare"
    },
    {
        name: "Skin B",
        price: 19.50,
        color: "Blue",
        rarity: "Common"
    },
    {
        name: "Skin C",
        price: 30.75,
        color: "Green",
        rarity: "Epic"
    },
    {
        name: "Skin D",
        price: 15.99,
        color: "Purple",
        rarity: "Uncommon"
    },
    {
        name: "Skin E",
        price: 22.49,
        color: "Gold",
        rarity: "Legendary"
    }
];

// Insert skins into the "skins" collection
db.skins.insertMany(skinsToInsert);

// Output the result
print("Skins inserted successfully!");
