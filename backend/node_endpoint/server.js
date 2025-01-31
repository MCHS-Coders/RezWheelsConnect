const express = require('express');
const mysql = require('mysql2/promise');
const map = require ('./map_endpoint');
const app = express();
const PORT = 5000;

// Middleware to parse JSON bodies
app.use(express.json());

// Database connection configuration
const dbConfig = {
    host: 'localhost',
    db_user: 'user',
    db_hash: '9f56e761d79bfdb34304a012586cb04d16b435ef6130091a97702e559260a2f2',
    database: 'DB_test'
};

// Endpoint to get a user's IP by username
app.post('/get_ip', async (req, res) => {
    try {
        const { user, password, target_user } = req.body;

        if (user.length >= 200 || password.length >= 200) {
            return res.status(400).json({ error: 'Too many characters in either the user name or password.'});
        }
  
        console.log("Username: ", user, "\nPassword: ", createHash('sha256').update(password).digest('base64'));
        if (user != dbConfig.db_user || password != Buffer.from(dbConfig.db_hash).toString('base64')) {
            console.log('Target Hash: ', dbConfig.db_hash)
            return res.status(400).json({ error: 'Invalid username or password, try again.' });
        }

        // Connect to the database
        const connection = await mysql.createConnection(dbConfig);

        // Query the database for the user's IP
        const [rows] = await connection.execute(
            'SELECT ip_address FROM users WHERE username = ?',
            [target_user]
        );

        // Close the database connection
        await connection.end();

        if (rows.length > 0) {
            // Return the IP address if found
            res.json({ status: 'success', ip_address: rows[0].ip_address });
        } else {
            // Handle case where the username is not found
            res.status(404).json({ error: 'Username not found.' });
        }
    } catch (error) {
        // Handle any database or server errors
        res.status(500).json({ error: 'An error occurred while retrieving the IP address.' });
        console.error(error);
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`API server is running on http://localhost:${PORT}`);
});
