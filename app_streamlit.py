import streamlit as st
import pandas as pd
from agenda import Agenda
from datetime import datetime as dt


# Streamlit session state kullanarak Agenda nesnesini saklıyoruz
if "agenda" not in st.session_state:
    st.session_state.agenda = Agenda()

agenda = st.session_state.agenda

# Sayfa ayarlarını yapılandır
st.set_page_config(page_title="Etkinlik Yönetim Sistemi", page_icon="🎉", layout="wide")

# Arka plan rengini ve diğer stil ayarlarını değiştirmek için CSS ekleyin
st.markdown(
    """
    <style>
    .stApp {
        background-color: #C8A2C8;  /* Arka plan rengi */
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #333;  /* Başlık rengi */
    }

    .stButton {
        background-color: #C8A2C8;  /* Buton arka plan rengi */
        color: white;  /* Buton metin rengi */
    }

    .stButton:hover {
        background-color: #45a049;  /* Buton üzerindeyken renk */
    }

    /* Sidebar başlık rengini ayarlama */
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3 {
        color: #C8A2C8;  /* Sidebar başlık rengi */
    }

    /* Tablo stilleri */
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }
    thead {
        background-color: #143d73; /* Başlık satırının rengi */
        color: green;
    }
    tbody tr:nth-child(even) {
        background-color: #143d73; /* Çift satırların arka plan rengi */
    }
    tbody tr:hover {
        background-color: #143d73 /* Üzerine gelindiğinde satır rengi */
    }
    tbody td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎉 Etkinlik Yönetim Sistemi")
st.sidebar.title("Seçenekler")

# Etkinlik Ekleme Formu
st.sidebar.header("Etkinlik Ekle")
name = st.sidebar.text_input("Etkinlik Adı:")
place = st.sidebar.text_input("Etkinlik Yeri:")
date = st.sidebar.text_input("Tarih (DD-MM-YYYY):")  # Tarihi metin girişi olarak alıyoruz
time = st.sidebar.text_input("Saat (HH:MM):")  # Zamanı metin girişi olarak alıyoruz

if st.sidebar.button("Etkinlik Ekle"):
    # Tarih formatını kontrol et
    try:
        formatted_date = dt.strptime(date, '%d-%m-%Y').strftime('%d-%m-%Y')  # Kullanıcıdan gelen tarihi doğrula
    except ValueError:
        st.error("Tarih formatı geçerli değil! Lütfen DD-MM-YYYY formatında girin.")
    else:
        # Saat formatını kontrol et
        try:
            formatted_time = dt.strptime(time, '%H:%M').strftime('%H:%M')  # Kullanıcıdan gelen saati doğrula
        except ValueError:
            st.error("Saat formatı geçerli değil! Lütfen HH:MM formatında girin.")
        else:
            # Etkinliği ekliyoruz
            agenda.add_event(name, place, formatted_date, formatted_time)
            st.success(f"Etkinlik eklendi: {name} - {formatted_date} - {formatted_time}")

# Etkinlikleri Görüntüle
st.header("Etkinlikleri Görüntüle")
if st.button("Etkinlikleri Listele"):
    if len(agenda.events) > 0:
        # display_events fonksiyonunu çağırmak yerine, DataFrame oluşturalım
        data = {
            "ID": list(range(1, len(agenda.events) + 1)),
            "Name": [event.name for event in agenda.events],
            "Place": [event.place for event in agenda.events],
            "Date": [event.date for event in agenda.events],
            "Time": [event.time for event in agenda.events]
        }

        event_df = pd.DataFrame(data)
        
        # Bu noktada tabloyu Streamlit'te gösteriyoruz
        st.table(event_df)  # ya da st.dataframe(event_df) ile etkileşimli tablo
    else:
        st.warning("Hiç etkinlik yok.")

# Etkinlik Arama
st.header("Etkinlik Ara")
search_id = st.number_input("Etkinlik ID'sini girin:", min_value=1, step=1)

if st.button("Etkinlik Ara"):
    event = agenda.search_event(search_id)  # Sonucu alıyoruz
    if event:
        st.write(f"Event Found:Name: {event.name}, Place: {event.place}, Date: {event.date}, Time: {event.time}")
    else:
        st.write("Aradığınız ID'ye sahip bir etkinlik bulunamadı.")
# Etkinlik Silme
st.header("Etkinlik Sil")
delete_id = st.number_input("Silmek istediğiniz etkinliğin ID'sini girin:", min_value=1, step=1)
if st.button("Etkinlik Sil"):
    agenda.delete_event(delete_id)
    st.success(f"Etkinlik silindi: {delete_id}")

# Etkinlik Güncelleme
st.header("Etkinlik Güncelle")
update_id = st.number_input("Güncellemek istediğiniz etkinliğin ID'sini girin:", min_value=1, step=1)
new_name = st.text_input("Yeni Etkinlik Adı:", "")
new_place = st.text_input("Yeni Etkinlik Yeri:", "")
new_date = st.text_input("Yeni Tarih (DD-MM-YYYY):", "")  # Kullanıcıdan alınan tarih doğrudan işleniyor
new_time = st.text_input("Yeni Saat (HH:MM):", "")  # Kullanıcıdan alınan saat doğrudan işleniyor

if st.button("Etkinliği Güncelle"):
    # Etkinliği güncelle, girilen değerler doğrudan kullanılıyor
    agenda.update_event(update_id, new_name=new_name, new_place=new_place, new_date=new_date, new_time=new_time)
    st.success(f"Etkinlik güncellendi: {update_id}. etkinlik !")
