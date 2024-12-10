import streamlit as st
from database import Session, Theater, Screen, ScreenType, Booking
from booking_system import BookingSystem
from datetime import datetime

def initialize():
    if 'booking_system' not in st.session_state:
        st.session_state.booking_system = BookingSystem()

def book_ticket():
    if not st.session_state.name:
        st.error("Please enter your name")
        return
    theater = st.session_state.booking_system.session.query(Theater).filter(
        Theater.name == st.session_state.theater
    ).first()
    screen_type_map = {
        "GOLD (₹400)": ScreenType.GOLD,
        "IMAX (₹300)": ScreenType.MAX,
        "General (₹200)": ScreenType.GENERAL
    }
    food_items = {}
    if st.session_state.popcorn > 0:
        food_items['popcorn'] = st.session_state.popcorn
    if st.session_state.sandwich > 0:
        food_items['sandwich'] = st.session_state.sandwich
    result, booking_id = st.session_state.booking_system.book_ticket(
        theater_id=theater.id,
        screen_type=screen_type_map[st.session_state.screen_type],
        user_name=st.session_state.name,
        food_items=food_items
    )
    if "successful" in result:
        st.success(f"Booking successful! ID: {booking_id}")
    else:
        st.warning(result)

def cancel_booking(booking_id):
    result = st.session_state.booking_system.cancel_ticket(booking_id)
    st.info(result)

def main():
    st.set_page_config(page_title="ShowTimeSync", layout="wide")
    initialize()
    st.title("ShowTimeSync")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Book Your Show")
        theaters = st.session_state.booking_system.session.query(Theater).all()
        theater_names = [theater.name for theater in theaters]
        st.selectbox("Select Theater", 
                    theater_names, 
                    key='theater')
        st.selectbox("Screen Type",
                    ["GOLD (₹400)", "IMAX (₹300)", "General (₹200)"],
                    key='screen_type')
        st.text_input("Name", key='name')
        st.subheader("Food & Beverages")
        col_food1, col_food2 = st.columns(2)
        with col_food1:
            st.number_input("Popcorn (₹150)", 
                          min_value=0, 
                          max_value=10, 
                          value=0,
                          key='popcorn')
        with col_food2:
            st.number_input("Sandwich (₹100)", 
                          min_value=0, 
                          max_value=10, 
                          value=0,
                          key='sandwich')

        if st.button("Book Now", type="primary"):
            book_ticket()
    with col2:
        st.subheader("Current Bookings")
        
        bookings = st.session_state.booking_system.session.query(Booking).filter(
            Booking.is_cancelled == False
        ).all()
        for booking in bookings:
            with st.expander(f"Booking ID: {booking.id}"):
                st.write(f"User: {booking.user_name}")
                st.write(f"Movie: {booking.screen.movie_name}")
                st.write(f"Screen: {booking.screen.screen_type.value}")
                st.write(f"Seat: {booking.seat_number}")
                if st.button("Cancel Booking", 
                           key=f"cancel_{booking.id}"):
                    cancel_booking(booking.id)
                    st.rerun()
    st.markdown("---")
    st.markdown(
        "<h6 style='text-align: center;'>Made with ❤️ by Tanish Poddar</h6>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()