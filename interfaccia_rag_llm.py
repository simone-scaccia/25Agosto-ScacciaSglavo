import streamlit as st
import os

# Crea un dizionario vuoto nella sessione streamlit
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files_content = {}

with st.sidebar:
    uploaded_files = st.file_uploader("Carica più file", type=["txt", "pdf"], accept_multiple_files=True)
    if uploaded_files:
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                # Aggiungi al dizionario uploaded_files_content come chiave il nome del file e come valore il suo contenuto
                st.session_state.uploaded_files_content[uploaded_file.name] = bytes_data
                #st.write("filename:", uploaded_file)
                #st.write(bytes_data)

#Stampa il dizionario
#st.write(st.session_state.uploaded_files_content)
    
    with st.form("Settings"):
        k = st.slider("Top k chunks", 0, 5, 1)

        #Fammi un select slider che permette di scegliere tra due opzioni
        
        search_type = st.select_slider("Scegli il tipo di ricerca", options=["MMR", "Similarity"])
        
        # Se seleziono "MMR" vissualizza un'altra slidebar che va da 0 ad 1
        if search_type == "MMR":
            mmr_value = st.slider("Seleziona il valore di MMR", 0.0, 1.0, 0.1,)

        chunk_size = st.slider("Seleziona la dimensinoe dei chunk", 0, 1000, 100)

        overlap = st.slider("Seleziona l'overlap", 0, 1000, 50)

        submit_button = st.form_submit_button("Confirm")

        if submit_button:
            st.session_state.k = k
            print(st.session_state)
            st.session_state.search_type = search_type
            if search_type == "MMR":
                st.session_state.mmr_value = mmr_value
            st.session_state.chunk_size = chunk_size
            st.session_state.overlap = overlap
            st.success("Settings saved!")
            
            save_dir = "one_piece_doc"
            os.makedirs(save_dir, exist_ok=True)  # Crea la cartella se non esiste

            for filename, content in st.session_state.uploaded_files_content.items():
                file_path = os.path.join(save_dir, filename)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content.decode("utf-8"))  # Decodifica da bytes a stringa
            
            # Chiama rag_faiss_lmstudio.py
            import rag_faiss_lmstudio
            rag_faiss_lmstudio.main()