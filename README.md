# ShowTimeSync

**ShowTimeSync** is a theater booking system that allows users to book movie tickets, view current bookings, and order food items (popcorn, sandwiches). It provides three different interfaces for interacting with the system:

1. **Normal Python Script (CLI)** - Simple command-line interaction.
2. **GUI (Tkinter)** - A rich graphical user interface for booking tickets.
3. **Web App (Streamlit)** - A modern web-based interface for booking and viewing current bookings.

## Features

- **Theater Booking**: Book tickets for different theaters and screen types (Gold, IMAX, and General).
- **Food Orders**: Order food items like popcorn and sandwiches with price discounts based on screen type.
- **Waiting List**: If the screen is full, users are added to a waiting list and notified when a seat becomes available.
- **Cancel Bookings**: Cancel tickets (if the show is more than 30 minutes away).
- **User-Friendly UI**: Interactive interfaces for booking and viewing bookings.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Normal Python](#normal-python)
  - [GUI](#gui)
  - [Streamlit](#streamlit)
- [Screenshots](#screenshots)
- [License](#license)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tanishpoddar/ShowTimeSync-MovieBookingSystem
   cd ShowTimeSync-MovieBookingSystem
   ```
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Before running the application, make sure you have MySQL installed and running on your machine.
   - Create a database `theater_db` in MySQL.
   - Replace the `username` and `password` in `database.py` with your MySQL credentials.
     ```python
     engine = create_engine('mysql://root:YOUR_PASSWORD@localhost/theater_db')
     ```

---

## Usage

### 1. Normal Python (CLI)
To run the application in the terminal (without GUI):

1. Run the following command to execute the Python script:
   ```bash
   python booking_system.py
   ```

2. This will allow you to interact with the booking system via the terminal. You can follow the on-screen prompts to book tickets.

### 2. GUI (Tkinter)
To run the graphical user interface with Tkinter:

1. Ensure you have the Tkinter library installed (it is included by default in most Python installations).
   
2. Run the following command:
   ```bash
   python gui-app.py
   ```

3. This will open the Tkinter window where you can interact with the booking system and view the current bookings.

### 3. Streamlit Web App
To run the web app using Streamlit:

1. Make sure you have Streamlit installed:
   ```bash
   pip install streamlit
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run streamlit-app.py
   ```

3. The web app will open in your browser, and you can book tickets and view the current bookings.

---

## Screenshots

### 1. Normal Python (CLI)
![CLI](images/cli.jpg)
![CLI](images/cli2.jpg)

### 2. GUI (Tkinter)

![GUI](images/gui.jpg)

This screenshot shows the Tkinter-based graphical user interface for booking movie tickets and ordering food.

### 3. Streamlit Web App

![Streamlit](images/streamlit.jpg)

This is the Streamlit-based web app for booking tickets. The user can select a theater, screen type, and food items, then book a ticket.

---
### Notes

- Make sure to replace the database credentials (`username`, `password`) in `database.py` before running the project.
- You can use `requirements.txt` for dependency management. Each mode should contain the necessary libraries (e.g., `streamlit`, `tkinter`, `sqlalchemy`, `mysql`, etc.).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
