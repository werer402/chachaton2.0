# %%
#!pip install streamlit

# %%
import streamlit as st

st.title("Мой первый Streamlit App")

st.write("Привет! Это простой frontend на Python с использованием Streamlit.")

name = st.text_input("Введите ваше имя:")
if name:
    st.write(f"Привет, {name}!")

if st.button("Нажми меня"):
    st.write("Кнопка нажата!")

# %% [markdown]
# ## Запуск Streamlit App
# 
# Чтобы запустить приложение, выполните в терминале:
# 
# ```bash
# streamlit run main.py
# ```
# 
# Но поскольку код в ноутбуке, сначала сохраните код в файл `app.py` и запустите его.


