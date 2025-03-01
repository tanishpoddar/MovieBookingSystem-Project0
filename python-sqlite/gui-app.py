import tkinter as tk
from tkinter import ttk, messagebox
from database import Session, Theater, Screen, ScreenType, Booking
from booking_system import BookingSystem
from datetime import datetime

class ShowTimeSync:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ShowTimeSync")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_styles()
        self.booking_system = BookingSystem()
        self.setup_ui()
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def setup_styles(self):
            colors = {
                'bg': '#0F172A',           
                'secondary_bg': '#1E293B',  
                'accent': '#334155',        
                'text': '#38BDF8',          
                'light_text': '#F1F5F9',    
                'button': '#0EA5E9',        
                'button_active': '#0284C7'  
            }
            self.style.configure('TFrame', background=colors['bg'])
            self.style.configure('Secondary.TFrame', background=colors['secondary_bg'])
            self.style.configure('TLabel', 
                            background=colors['bg'],
                            foreground=colors['light_text'])
            self.style.configure('Header.TLabel',
                            background=colors['bg'],
                            foreground=colors['text'],
                            font=('Arial', 30, 'bold'))
            self.style.configure('Subheader.TLabel',
                            background=colors['secondary_bg'],
                            foreground=colors['text'],
                            font=('Arial', 18, 'bold'))
            self.style.configure('Form.TLabel',
                            background=colors['secondary_bg'],
                            foreground=colors['light_text'],
                            font=('Arial', 12))
            self.style.configure('TButton',
                            background=colors['button'],
                            foreground=colors['light_text'],
                            padding=12,
                            font=('Arial', 12, 'bold'))
            self.style.map('TButton',
                        background=[('active', colors['button_active'])])
            self.style.configure('Booking.TFrame',
                            background=colors['accent'],
                            relief='raised')
            self.style.configure('TEntry',
                            fieldbackground=colors['secondary_bg'],
                            foreground=colors['light_text'],
                            padding=10)
            self.style.configure('TCombobox',
                            fieldbackground=colors['secondary_bg'],
                            foreground=colors['light_text'],
                            padding=10)
            self.style.configure('TSpinbox',
                            fieldbackground=colors['secondary_bg'],
                            foreground=colors['light_text'],
                            padding=10)

    def setup_ui(self):
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        header = ttk.Label(main_container, text="ShowTimeSync", style='Header.TLabel')
        header.grid(row=0, column=0, pady=10)
        content = ttk.Frame(main_container)
        content.grid(row=1, column=0, sticky="nsew", pady=10)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        booking_frame = ttk.Frame(content, style='Secondary.TFrame')
        booking_frame.grid(row=0, column=0, sticky="nsew", padx=5)
        booking_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(booking_frame, text="Book Your Show", style='Subheader.TLabel').grid(row=0, column=0, pady=10)
        form_style = {'padx': 10, 'pady': 5}
        theater_frame = ttk.Frame(booking_frame, style='Secondary.TFrame')
        theater_frame.grid(row=1, column=0, sticky="ew", **form_style)
        theater_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(theater_frame, text="Select Theater:", style='Form.TLabel').grid(row=0, column=0)
        self.theater_var = tk.StringVar()
        theaters = self.booking_system.session.query(Theater).all()
        theater_names = [theater.name for theater in theaters]
        ttk.Combobox(theater_frame, textvariable=self.theater_var, values=theater_names, width=25).grid(
            row=0, column=1, padx=5, sticky="ew")
        screen_frame = ttk.Frame(booking_frame, style='Secondary.TFrame')
        screen_frame.grid(row=2, column=0, sticky="ew", **form_style)
        screen_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(screen_frame, text="Screen Type:", style='Form.TLabel').grid(row=0, column=0)
        self.screen_var = tk.StringVar()
        ttk.Combobox(screen_frame, textvariable=self.screen_var,
                    values=["GOLD (₹400)", "IMAX (₹300)", "General (₹200)"], width=25).grid(
                        row=0, column=1, padx=5, sticky="ew")
        name_frame = ttk.Frame(booking_frame, style='Secondary.TFrame')
        name_frame.grid(row=3, column=0, sticky="ew", **form_style)
        name_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(name_frame, text="Name:", style='Form.TLabel').grid(row=0, column=0)
        self.name_entry = ttk.Entry(name_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, sticky="ew")
        food_frame = ttk.Frame(booking_frame, style='Secondary.TFrame')
        food_frame.grid(row=4, column=0, sticky="ew", **form_style)
        food_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(food_frame, text="Food & Beverages", style='Subheader.TLabel').grid(row=0, column=0, pady=10)
        popcorn_frame = ttk.Frame(food_frame, style='Secondary.TFrame')
        popcorn_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=10)
        popcorn_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(popcorn_frame, text="Popcorn (₹150):", style='Form.TLabel').grid(row=0, column=0)
        self.popcorn_var = tk.StringVar(value="0")
        ttk.Spinbox(popcorn_frame, from_=0, to=10, textvariable=self.popcorn_var, width=8).grid(row=0, column=1, sticky="e")
        sandwich_frame = ttk.Frame(food_frame, style='Secondary.TFrame')
        sandwich_frame.grid(row=2, column=0, sticky="ew", pady=5, padx=10)
        sandwich_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(sandwich_frame, text="Sandwich (₹100):", style='Form.TLabel').grid(row=0, column=0)
        self.sandwich_var = tk.StringVar(value="0")
        ttk.Spinbox(sandwich_frame, from_=0, to=10, textvariable=self.sandwich_var, width=8).grid(row=0, column=1, sticky="e")
        tk.Button(booking_frame, text="Book Now", command=self.book_ticket,
                    bg='#0EA5E9', fg='white', font=('Arial', 12, 'bold')).grid(
                        row=5, column=0, pady=20, padx=10, sticky="ew")
        bookings_frame = ttk.Frame(content, style='Secondary.TFrame')
        bookings_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        bookings_frame.grid_columnconfigure(0, weight=1)
        bookings_frame.grid_rowconfigure(1, weight=1)
        ttk.Label(bookings_frame, text="Current Bookings", style='Subheader.TLabel').grid(row=0, column=0, pady=10)
        self.bookings_canvas = tk.Canvas(bookings_frame, bg='#16213e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(bookings_frame, orient=tk.VERTICAL, command=self.bookings_canvas.yview)
        self.bookings_list = ttk.Frame(self.bookings_canvas, style='Secondary.TFrame')
        self.bookings_list.bind("<Configure>",
            lambda e: self.bookings_canvas.configure(scrollregion=self.bookings_canvas.bbox("all")))
        self.bookings_canvas.create_window((0, 0), window=self.bookings_list, anchor="nw")
        self.bookings_canvas.configure(yscrollcommand=scrollbar.set)
        self.bookings_canvas.grid(row=1, column=0, sticky="nsew", padx=5)
        scrollbar.grid(row=1, column=1, sticky="ns")
        footer = ttk.Label(main_container, text="Made with ❤️ by Tanish Poddar",
                            style='TLabel', font=('Arial', 12), foreground='#38BDF8')
        footer.grid(row=2, column=0, pady=10)
        self.update_bookings()

    def book_ticket(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        theater = self.booking_system.session.query(Theater).filter(
            Theater.name == self.theater_var.get()
        ).first()
        screen_type_map = {
            "GOLD (₹400)": ScreenType.GOLD,
            "IMAX (₹300)": ScreenType.MAX,
            "General (₹200)": ScreenType.GENERAL
        }
        screen_type = screen_type_map[self.screen_var.get()]
        food_items = {}
        popcorn_qty = int(self.popcorn_var.get())
        sandwich_qty = int(self.sandwich_var.get())
        if popcorn_qty > 0:
            food_items['popcorn'] = popcorn_qty
        if sandwich_qty > 0:
            food_items['sandwich'] = sandwich_qty
        result, booking_id = self.booking_system.book_ticket(
            theater_id=theater.id,
            screen_type=screen_type,
            user_name=name,
            food_items=food_items
        )
        if "successful" in result:
            messagebox.showinfo("Success", f"Booking successful! ID: {booking_id}")
            self.update_bookings()
        else:
            messagebox.showwarning("Notice", result)

    def update_bookings(self):
        for widget in self.bookings_list.winfo_children():
            widget.destroy()

        bookings = self.booking_system.session.query(Booking).filter(
            Booking.is_cancelled == False
        ).all()
        for booking in bookings:
            booking_frame = ttk.Frame(self.bookings_list, style='Booking.TFrame')
            booking_frame.pack(fill=tk.X, pady=2, padx=5)
            info_text = f"ID: {booking.id}\nUser: {booking.user_name}\nMovie: {booking.screen.movie_name}\nScreen: {booking.screen.screen_type.value}\nSeat: {booking.seat_number}"
            ttk.Label(booking_frame, text=info_text, style='TLabel').pack(side=tk.LEFT, padx=5)
            ttk.Button(booking_frame, text="Cancel", command=lambda b=booking: self.cancel_booking(b.id)).pack(
                side=tk.RIGHT, padx=5)

    def cancel_booking(self, booking_id):
        result = self.booking_system.cancel_ticket(booking_id)
        messagebox.showinfo("Cancellation", result)
        self.update_bookings()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ShowTimeSync()
    app.run()