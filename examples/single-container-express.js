const express = require('express');
const path = require('path');
const app = express();

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'frontend/build')));

// API Routes
app.post('/api/admin/login', (req, res) => {
  // Your login logic here
  res.json({ message: 'Login endpoint' });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Catch all handler: send back React's index.html file for client-side routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/build', 'index.html'));
});

const port = process.env.PORT || 8000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
