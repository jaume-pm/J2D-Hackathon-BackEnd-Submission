# J2D-Hackathon-BackEnd-Submission 🚀

## Project Overview 🌐
Developed for the J2D Microhackathon, this backend API offers users a platform to interact with virtual skins, manage their in-app balance, and benefit from numerous features.

### Unique Features & Decisions 🛠️
- **Extended Functionality**: This project introduces sophisticated user management and a detailed economic model, going beyond the main requirements.
- **Balance Management**: Actions like purchasing or selling a skin impact the user's balance immediately. 💰
- **Route Update**: Modified the route from `/skins/avaible` to `/skins/available` to address a potential typo.
- **Docker Integration**: The project is dockerized for streamlined deployment and setup. 🐳 It also includes a Mongo Express Docker configuration for an enhanced visualization of the MongoDB database.
- **Database Initialization**: MongoDB scripts (`insert_skins.js` and `insert_users.js`) preload data, ensuring a rich experience right from the start.

## Data Models 📊
### 1. **Skin**: Virtual skin attributes:
   - `name`: Distinctive name.
   - `price`: Skin cost.
   - `color`: Default color.
   - `rarity`: Rarity level.
  
### 2. **User**: User-specific attributes:
   - `username`: Unique identifier.
   - `email`: Contact email.
   - `password`: Encrypted password.
   - `balance`: Current monetary balance.
   - `owned_skins`: List of skins owned by the user, including:
     - `skin_id`: Identifier.
     - `color`: Current color.

## API Endpoints 📡
1. **GET /skins/available**: 
   - **Returns**: List of available skins.
     - Successful Response: `{"result": "ok", "skins": [skins_data]}`
     - Error Response: `{"error": error_message}`
  
2. **POST /skins/buy**: 
   - **Required JSON**: `{"user_id": "user_object_id", "skin_id": "skin_object_id"}`
     - Successful Response: `{"result": "ok"}`
     - Error Response: `{"error": error_message}`
   
3. **GET /skins/myskins**: 
   - **Required JSON**: `{"user_id": "user_object_id"}`
   - **Returns**: List of skins owned by the user, including skin ID, name, color, and rarity.
     - Successful Response: `{"result": "ok", "skins": [user_skin_info]}`
     - Error Response: `{"error": error_message}`
  
4. **PUT /skins/color**: 
   - **Required JSON**: `{"user_id": "user_object_id", "skin_id": "skin_object_id", "color": "desired_color"}`
     - Successful Response: `{"result": "ok"}`
     - Error Response: `{"error": error_message}`
  
5. **DELETE /skins/delete/<skin_id>**: 
   - **Required JSON**: `{"user_id": "user_object_id"}`
     - Successful Response: `{"result": "ok"}`
     - Error Response: `{"error": error_message}`
  
6. **GET /skin/getskin/<skin_id>**: 
   - **Returns**: Details of a specific skin, including skin ID, name, color, and rarity.
     - Successful Response: `{"result": "ok", "skin": skin_data}`
     - Error Response: `{"error": error_message}`
  
7. **POST /add_skins**: 
  - **Required JSON**: `{"file": "JSON_file"}`
   - **Required**: A file uploaded with the request. JSON_file must contain all the information of the skins that are wished to be added.
     - Successful Response: `{"result": "ok"}`
     - Error Response: `{"error": error_message}`

## File Descriptions 📂
- **API**:
  - **Dockerfile**: Docker setup for the API.
  - **app.py**: Main entry for the application.
  - **controller_skins.py**: Handles skin-related operations.
  - **models.py**: Data model definitions and DB connections.
  - **requirements.txt**: Python package dependencies.
  - **route.py**: API routes definitions.
  - **economy.py**: Configurations related to economic transactions.
  - **getters.py**: Utility functions for data retrieval and validation.

- **MONGO**:
  - **Dockerfile**: MongoDB Docker configuration.
  - **insert_skins.js & insert_users.js**: Database seeding scripts.
  - **data**: Docker volume where the database is stored.

## Setup & Running 🚦
1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project root.
3. Run the following command:
```bash
docker-compose -f flask-docker-compose.yml up
```

4. Interact with the API at [http://localhost:17011](http://localhost:17011) and manage MongoDB at [http://localhost:8081](http://localhost:8081) using the credentials:

   - **Username**: jump2digital
   - **Password**: 17112023 (The day of the Hackathon 👀)

---

### Conclusion 🎉
Thanks for checking out this project! I've poured a lot of energy and passion into this, and I hope it shines through. Can't wait to see what everyone brings to the table at the hackathon! Catch you there! 🚀🔥
