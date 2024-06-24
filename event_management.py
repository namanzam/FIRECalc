import streamlit as st

def add_event():
    event = {'type': st.session_state['event_type'], 'age': st.session_state['event_age']}
    if st.session_state['event_type'] == "House":
        event['price'] = st.session_state['event_price']
    elif st.session_state['event_type'] == "Car":
        event['price'] = st.session_state['event_price']
    elif st.session_state['event_type'] == "Wedding":
        event['cost'] = st.session_state['event_cost']
    elif st.session_state['event_type'] == "Kid":
        event['yearly_cost'] = st.session_state['event_yearly_cost']
        event['college_cost'] = st.session_state['event_college_cost']
    st.session_state['big_events'].append(event)

def remove_event(index):
    st.session_state['big_events'].pop(index)

def edit_event(index):
    event = st.session_state['big_events'][index]
    st.session_state['event_type'] = event['type']
    st.session_state['event_age'] = event['age']
    if event['type'] == "House":
        st.session_state['event_price'] = event['price']
    elif event['type'] == "Car":
        st.session_state['event_price'] = event['price']
    elif event['type'] == "Wedding":
        st.session_state['event_cost'] = event['cost']
    elif event['type'] == "Kid":
        st.session_state['event_yearly_cost'] = event['yearly_cost']
        st.session_state['event_college_cost'] = event['college_cost']
    st.session_state['edit_index'] = index

def update_event():
    index = st.session_state['edit_index']
    event = st.session_state['big_events'][index]
    event['type'] = st.session_state['event_type']
    event['age'] = st.session_state['event_age']
    if event['type'] == "House":
        event['price'] = st.session_state['event_price']
    elif event['type'] == "Car":
        event['price'] = st.session_state['event_price']
    elif event['type'] == "Wedding":
        event['cost'] = st.session_state['event_cost']
    elif event['type'] == "Kid":
        event['yearly_cost'] = st.session_state['event_yearly_cost']
        event['college_cost'] = st.session_state['event_college_cost']
    st.session_state['big_events'][index] = event
    st.session_state.pop('edit_index')
