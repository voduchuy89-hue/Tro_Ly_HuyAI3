import streamlit as st
import ollama

st.title("Ollama x Streamlit Chatbot 🤖")

# Khởi tạo lịch sử trò chuyện
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập liệu từ người dùng
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    # Thêm tin nhắn người dùng vào lịch sử
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Phản hồi từ Ollama
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Gọi mô hình (ở đây dùng llama3, bạn có thể đổi thành mô hình bạn có)
        response = ollama.chat(
            model='llama3',
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in response:
            full_response += chunk['message']['content']
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})