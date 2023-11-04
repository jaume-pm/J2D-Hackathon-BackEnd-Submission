// Connect to the MongoDB server
var conn = new Mongo();
var db = conn.getDB("J2D"); // Change to your database name

// Array of available colors
var colors = ["Red", "Blue", "Green", "Purple", "Gold"];

// Function to get a random element from an array
function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

// Function to generate a random color
function getRandomColor() {
    return getRandomElement(colors);
}

function getRandomSkinId() {
    var randomSkinCursor = db.skins.aggregate([{ $sample: { size: 1 } }]); // Get random skin cursor
    return randomSkinCursor.toArray()[0]._id; // Get random skin _id
}


// Users data to be inserted
var usersToInsert = [
    {
        username: "john_doe",
        email: "john.doe@example.com",
        password: "hashedpassword123",
        balance: 150.25,
        owned_skins: [
            {
                skin_id: getRandomSkinId(),
                color: getRandomColor()
            }
        ]
    },
    {
        username: "jane_smith",
        email: "jane.smith@example.com",
        password: "securehashedpass456",
        balance: 75.50,
        owned_skins: [
            {
                skin_id: getRandomSkinId(),
                color: getRandomColor()
            }
        ]
    },
    {
        username: "alex_jones",
        email: "alex.jones@example.com",
        password: "supersecretword789",
        balance: 120.75,
        owned_skins: [
            {
                skin_id: getRandomSkinId(),
                color: getRandomColor()
            }
        ]
    }
];

// Insert users into the "users" collection
db.users.insertMany(usersToInsert);

// Output the result
print("Users inserted successfully!");
