const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const moment = require('moment');
const bodyParser = require('body-parser');
const session = require('express-session');

// Initialize SQLite database (in-memory, replace with a persistent DB if needed)
const db = new sqlite3.Database(':memory:');

// Initialize the database schema for users and events
db.serialize(() => {
    db.run("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)");
    db.run("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, title TEXT, description TEXT, date TEXT, time TEXT, FOREIGN KEY(user_id) REFERENCES users(id))");
});

// Helper function to format datetime
function formatDateTime(date, time) {
    return moment(`${date} ${time}`, 'YYYY-MM-DD HH:mm').format();
}

// Register user
function registerUser(username, password) {
    return new Promise((resolve, reject) => {
        bcrypt.hash(password, 10, (err, hashedPassword) => {
            if (err) return reject('Error hashing password.');
            const stmt = db.prepare("INSERT INTO users (username, password) VALUES (?, ?)");
            stmt.run(username, hashedPassword, function(err) {
                if (err) return reject('Error registering user.');
                resolve({ id: this.lastID, username });
            });
            stmt.finalize();
        });
    });
}

// Login user
function loginUser(username, password) {
    return new Promise((resolve, reject) => {
        db.get("SELECT * FROM users WHERE username = ?", [username], (err, user) => {
            if (err || !user) return reject('User not found.');
            bcrypt.compare(password, user.password, (err, match) => {
                if (err || !match) return reject('Invalid password.');
                resolve(user);
            });
        });
    });
}

// Add an event
function addEvent(userId, title, description, date, time) {
    const eventDateTime = formatDateTime(date, time);
    return new Promise((resolve, reject) => {
        const stmt = db.prepare("INSERT INTO events (user_id, title, description, date, time) VALUES (?, ?, ?, ?, ?)");
        stmt.run(userId, title, description, eventDateTime, time, function (err) {
            if (err) return reject('Failed to add event.');
            resolve({ id: this.lastID, userId, title, description, date: eventDateTime, time });
        });
        stmt.finalize();
    });
}

// Get all events for a user
function getEvents(userId) {
    return new Promise((resolve, reject) => {
        db.all("SELECT * FROM events WHERE user_id = ?", [userId], (err, rows) => {
            if (err) return reject('Failed to retrieve events.');
            resolve(rows);
        });
    });
}

// Update the event's date
function addDate(eventId, newDate) {
    return new Promise((resolve, reject) => {
        const newDateTime = formatDateTime(newDate, null);  // Null for time, so we only update the date
        db.run("UPDATE events SET date = ? WHERE id = ?", [newDateTime, eventId], function (err) {
            if (err) return reject('Failed to update date.');
            if (this.changes === 0) return reject('Event not found.');
            resolve(`Date updated for event ID: ${eventId}`);
        });
    });
}

// Update the event's time
function addTime(eventId, newTime) {
    return new Promise((resolve, reject) => {
        const stmt = db.prepare("UPDATE events SET time = ? WHERE id = ?");
        stmt.run(newTime, eventId, function (err) {
            if (err) return reject('Failed to update time.');
            if (this.changes === 0) return reject('Event not found.');
            resolve(`Time updated for event ID: ${eventId}`);
        });
        stmt.finalize();
    });
}

// Remove the date from the event (set it to null)
function removeDate(eventId) {
    return new Promise((resolve, reject) => {
        db.run("UPDATE events SET date = NULL WHERE id = ?", eventId, function (err) {
            if (err) return reject('Failed to remove date.');
            if (this.changes === 0) return reject('Event not found.');
            resolve(`Date removed for event ID: ${eventId}`);
        });
    });
}

// Remove the time from the event (set it to null)
function removeTime(eventId) {
    return new Promise((resolve, reject) => {
        db.run("UPDATE events SET time = NULL WHERE id = ?", eventId, function (err) {
            if (err) return reject('Failed to remove time.');
            if (this.changes === 0) return reject('Event not found.');
            resolve(`Time removed for event ID: ${eventId}`);
        });
    });
}

// Export functions to be used in other files (like the main server file)
module.exports = {
    registerUser,
    loginUser,
    addEvent,
    getEvents,
    addDate,
    addTime,
    removeDate,
    removeTime
};
