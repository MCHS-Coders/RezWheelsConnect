const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const calendarHelper = require('./cal'); // Import the helper module

const app = express();
const port = 5000;

// Middleware to parse JSON requests
app.use(bodyParser.json());

// Middleware for handling user sessions
app.use(session({
    secret: 'ASuperSecretKey',  // Replace with a secure secret key
    resave: false,
    saveUninitialized: true
}));

// Middleware to ensure the user is authenticated (used for protected routes)
function isAuthenticated(req, res, next) {
    if (req.session.userId) {
        return next();
    }
    res.status(401).json({ error: 'Unauthorized. Please log in.' });
}

// Endpoint for registering a new user
app.post('/register', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required.' });
    }

    try {
        const user = await calendarHelper.registerUser(username, password);
        res.status(201).json({ message: 'User registered successfully', user });
    } catch (error) {
        res.status(500).json({ error: 'Error registering user.' });
    }
});

// Endpoint for logging in
app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required.' });
    }

    try {
        const user = await calendarHelper.loginUser(username, password);
        if (!user) {
            return res.status(401).json({ error: 'Invalid credentials.' });
        }
        req.session.userId = user.id;  // Store user ID in session
        res.status(200).json({ message: 'Login successful', user });
    } catch (error) {
        res.status(500).json({ error: 'Error during login.' });
    }
});

// Endpoint to log out the user and destroy the session
app.post('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            return res.status(500).json({ error: 'Error logging out.' });
        }
        res.status(200).json({ message: 'Logged out successfully.' });
    });
});

// Endpoint to add an event (requires authentication)
app.post('/events', isAuthenticated, async (req, res) => {
    const { title, description, date, time } = req.body;
    const userId = req.session.userId;

    if (!title || !description || !date || !time) {
        return res.status(400).json({ error: 'Title, description, date, and time are required.' });
    }

    try {
        const event = await calendarHelper.addEvent(userId, title, description, date, time);
        res.status(201).json({ message: 'Event added successfully', event });
    } catch (error) {
        res.status(500).json({ error: 'Error adding event.' });
    }
});

// Endpoint to get all events for the logged-in user
app.get('/events', isAuthenticated, async (req, res) => {
    const userId = req.session.userId;

    try {
        const events = await calendarHelper.getEvents(userId);
        res.status(200).json({ events });
    } catch (error) {
        res.status(500).json({ error: 'Error retrieving events.' });
    }
});

// Endpoint to update the date of an event
app.put('/events/:id/date', isAuthenticated, async (req, res) => {
    const { id } = req.params;
    const { newDate } = req.body;

    if (!newDate) {
        return res.status(400).json({ error: 'New date is required.' });
    }

    try {
        const result = await calendarHelper.addDate(id, newDate);
        res.status(200).json({ message: result });
    } catch (error) {
        res.status(500).json({ error: 'Error updating event date.' });
    }
});

// Endpoint to update the time of an event
app.put('/events/:id/time', isAuthenticated, async (req, res) => {
    const { id } = req.params;
    const { newTime } = req.body;

    if (!newTime) {
        return res.status(400).json({ error: 'New time is required.' });
    }

    try {
        const result = await calendarHelper.addTime(id, newTime);
        res.status(200).json({ message: result });
    } catch (error) {
        res.status(500).json({ error: 'Error updating event time.' });
    }
});

// Endpoint to remove the date from an event
app.put('/events/:id/remove-date', isAuthenticated, async (req, res) => {
    const { id } = req.params;

    try {
        const result = await calendarHelper.removeDate(id);
        res.status(200).json({ message: result });
    } catch (error) {
        res.status(500).json({ error: 'Error removing event date.' });
    }
});

// Endpoint to remove the time from an event
app.put('/events/:id/remove-time', isAuthenticated, async (req, res) => {
    const { id } = req.params;

    try {
        const result = await calendarHelper.removeTime(id);
        res.status(200).json({ message: result });
    } catch (error) {
        res.status(500).json({ error: 'Error removing event time.' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
