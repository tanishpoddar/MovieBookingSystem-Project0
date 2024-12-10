const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

// Read the SQL file
const initSQL = fs.readFileSync('./init.sql', 'utf8');

// Connect to database
const db = new sqlite3.Database('movie_booking.db');

// Execute initialization SQL
db.serialize(() => {
    // Split the SQL file into individual statements
    const statements = initSQL.split(';').filter(stmt => stmt.trim());
    
    // Execute each statement
    statements.forEach(statement => {
        if (statement.trim()) {
            db.run(statement, err => {
                if (err) {
                    console.error('Error executing statement:', err);
                    console.error('Statement:', statement);
                }
            });
        }
    });

    // Initialize seats for each screen
    db.all('SELECT id, total_seats FROM screens', [], (err, screens) => {
        if (err) {
            console.error('Error getting screens:', err);
            return;
        }

        screens.forEach(screen => {
            for (let i = 1; i <= screen.total_seats; i++) {
                db.run(
                    'INSERT INTO seats (screen_id, seat_number) VALUES (?, ?)',
                    [screen.id, `A${i}`],
                    err => {
                        if (err) {
                            console.error('Error inserting seat:', err);
                        }
                    }
                );
            }
        });
    });
});

console.log('Database initialization completed');