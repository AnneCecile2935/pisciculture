### 7 **Sequence Diagrams**
#### 7.1 **Sequence Diagram "User Authentication":**
![Sequence diagram authentication](../images/seq_diag_auth.png)
##### 7.1.1 **Credential Input**
- The user enters their **email** and **password** in a form.
- Clicks the **"Log In"** button.
##### 7.1.2 **Front-end Validation**
- The front-end checks that email and password are not empty.
- If any field is empty, an error message appears immediately.
##### 7.1.3 **Authentication Request**
- The front-end sends a **POST** request to `/api/auth/login/` with the data:
  ```json
  {
      "email": "user@example.com",
      "password": "password123"
  }

##### 7.1.4 Database Verification

- The back-end queries the user by email:
	```postgresql
  SELECT id, email, password, role FROM utilisateur WHERE email='user@example.com';
  ```

- If the user does not exist, returns a 401 Unauthorized error.

##### 7.1.5 Password Verification

- The back-end compares the provided password with the stored hash (using Django's check_password).
If the password is invalid, returns a 401 Unauthorized error.

##### 7.1.6 JWT Token Generation

- If authentication succeeds, the back-end generates a JWT token containing:

user_id: 1
role: "employee" (or "manager"/"admin")
exp: expiration date (e.g., +24h).

##### 7.1.7 Response and Token Storage

- The back-end returns the token and user details:
	```json
  {
      "token": "xyz123.abc456.def789",
      "user": {
          "id": 1,
          "email": "user@example.com",
          "role": "employé"
      }
  }
  ```

- The front-end stores the token in localStorage and redirects the user to the home page.

##### 7.1.8 Error Handling

- Empty email/password: Front-end error message.
- Invalid email/password: Back-end 401 Unauthorized error.

#### 7.2 Sequence Diagram "Recording a Feeding"

![diagramme de séquence enregistrer un repas](../images/seq_diag_enregistrer_repas.png)

###### Site Selection

- The user selects a site (e.g., "Valley Site").
- The front-end requests the list of ponds associated with this site via GET /api/sites/{site_id}/ponds/.

###### Pond Display

- The back-end checks permissions (valid JWT token) and returns the list of available ponds.
- The user sees the ponds in a dropdown menu and selects one (e.g., "Pond A").

###### Data Entry

- The user fills out the form:

- Feed type (e.g., "pellets").
- Distributed quantity (e.g., 500g).


- Clicks "Submit" to send the form.

###### Front-end Validation

- The front-end checks if the data is valid (e.g., quantity > 0, feed selected).
- If invalid: Displays an error message (e.g., "Please enter the quantity").
- If valid: Sends the data to the back-end via POST /api/feedings/.

###### Back-end Processing

- The back-end:

- Verifies the JWT token and user permissions.
- Confirms the selected pond exists and is accessible to the user.
- If access denied: Returns a 403 Forbidden error ("Access denied to this pond").
- If access granted: Saves the feeding record to the database.

###### Confirmation

- The back-end returns a 201 Created response with the feeding details.
- The front-end displays a success message: "Feeding recorded for LOT-001".
