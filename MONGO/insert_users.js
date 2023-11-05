// Connect to the MongoDB server
var conn = new Mongo();
var db = conn.getDB("J2D"); // Change to your database name

// Array of available colors
var colors = ["Red", "Blue", "Green", "Purple", "Gold", "Black"];

// Function to get a random element from an array
function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

// Function to generate a random color
function getRandomColor() {
    return getRandomElement(colors);
}

// Function to generate an array of n random skin IDs
function getRandomSkinIds(n) {
    var randomSkinCursor = db.skins.aggregate([{ $sample: { size: n } }]); // Get random skin cursor
    return randomSkinCursor.toArray().map(function(skin) {
        return skin._id; // Get random skin _id
    });
}

alex_skins = getRandomSkinIds(2)

// Users data to be inserted
var usersToInsert = [
    {
        username: "PhoenixRider89",
        email: "john.doe@example.com",
        password: "hashedpassword123",
        balance: 150.25,
        owned_skins: [
            {
                skin_id: getRandomSkinIds(1)[0],
                color: getRandomColor()
            }
        ]
    },
    {
        username: "ShadowWalker23",
        email: "jane.smith@example.com",
        password: "securehashedpass456",
        balance: 75.50,
        owned_skins: [
            {
                skin_id: getRandomSkinIds(1)[0],
                color: getRandomColor()
            }
        ]
    },
    {
        username: "ChronoMasterX",
        email: "alex.jones@example.com",
        password: "supersecretword789",
        balance: 120.75,
        owned_skins: [
            {
                skin_id: alex_skins[0],
                color: getRandomColor()
            },
            {
                skin_id: alex_skins[1],
                color: getRandomColor()
            }
        ]
    }
];


// Insert users into the "users" collection
db.users.insertMany(usersToInsert);
