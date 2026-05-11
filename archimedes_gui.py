import os
import threading
from PIL import Image, ImageDraw
import customtkinter as ctk
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# --- Professional Dark Theme Configuration ---
ctk.set_appearance_mode("dark")

class ArchimedesPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Window Setup & Branding
        # Using the stylized Lambda 'Λ' for that Noir aesthetic
        self.title(" ΛRCHIMEDES | OFFLINE AI RAG")
        self.geometry("1000x750")
        self.configure(fg_color="#121212") # Deep charcoal background

        # --- Auto-Generate & Set Window Icon ---
        icon_path = "archimedes_icon.ico"
        if not os.path.exists(icon_path):
            # Create a 64x64 dark charcoal image
            icon_img = Image.new('RGBA', (64, 64), (18, 18, 18, 255))
            draw = ImageDraw.Draw(icon_img)
            # Draw a sleek white 'Λ' (Lambda)
            draw.line([(32, 16), (16, 48)], fill=(224, 224, 224, 255), width=6)
            draw.line([(32, 16), (48, 48)], fill=(224, 224, 224, 255), width=6)
            icon_img.save(icon_path)
        
        # Apply the icon (using .after ensures it overrides the default Tkinter icon safely)
        self.after(200, lambda: self.iconbitmap(icon_path))

        # 2. Backend Initialization (Optimized for your 8GB RAM)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db = Chroma(persist_directory="./db", embedding_function=self.embeddings)
        self.llm = Ollama(model="llama3.2:3b")
        
        # RetrievalQA setup with k=5 for better context retrieval (fixes the math formula issue)
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 5})
        )

        # 3. UI Layout Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER SECTION ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 20))
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame, 
            text="ΛRCHIMEDES", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold"),
            text_color="#E0E0E0"
        )
        self.logo_label.pack(side="left")

        self.tagline = ctk.CTkLabel(
            self.header_frame, 
            text=" // DOCUMENT INTELLIGENCE", 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#666666"
        )
        self.tagline.pack(side="left", padx=15, pady=(8, 0))

        # --- CHAT AREA (Monospaced Console Style) ---
        self.chat_display = ctk.CTkTextbox(
            self, 
            font=("Consolas", 14), 
            fg_color="#1a1a1a", 
            border_color="#333333",
            border_width=1,
            text_color="#CCCCCC"
        )
        self.chat_display.grid(row=1, column=0, padx=40, pady=10, sticky="nsew")
        self.chat_display.insert("0.0", "SYSTEM READY. SOURCE: TITAN VISION CORE.\n" + ("-"*40) + "\n\n")
        self.chat_display.configure(state="disabled")

        # --- INPUT AREA ---
        self.input_container = ctk.CTkFrame(self, fg_color="transparent")
        self.input_container.grid(row=2, column=0, padx=40, pady=(20, 40), sticky="ew")
        self.input_container.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(
            self.input_container, 
            placeholder_text="Query technical documentation...",
            height=50,
            fg_color="#1a1a1a",
            border_color="#333333",
            text_color="#FFFFFF"
        )
        self.user_input.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        
        # Bind Enter key to start query
        self.user_input.bind("<Return>", lambda e: self.start_query_thread())

        self.send_btn = ctk.CTkButton(
            self.input_container, 
            text="EXECUTE", 
            width=120, 
            height=50,
            fg_color="#2b2b2b",
            hover_color="#3d3d3d",
            text_color="#FFFFFF",
            font=ctk.CTkFont(weight="bold"),
            command=self.start_query_thread
        )
        self.send_btn.grid(row=0, column=1)

    # --- Logic Methods ---

    def start_query_thread(self):
        """Launches the AI processing in a separate thread to keep UI responsive."""
        query = self.user_input.get()
        if query:
            self.user_input.delete(0, 'end')
            self.update_chat(f"USER_QUERY > {query}\n")
            
            thread = threading.Thread(target=self.process_query, args=(query,))
            thread.start()

    def update_chat(self, message):
        """Helper to safely update the disabled textbox."""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message)
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def process_query(self, query):
        """Handles the RAG retrieval and LLM generation via Ollama."""
        self.update_chat("ARCHIMEDES > PROCESSING...\n")
        
        try:
            response = self.qa_chain.invoke(query)
            
            self.chat_display.configure(state="normal")
            # Remove the 'PROCESSING' line before showing answer
            self.chat_display.delete("end-2l", "end-1l") 
            self.update_chat(f"ARCHIMEDES > {response['result']}\n\n")
        except Exception as e:
            self.update_chat(f"SYSTEM_ERROR > Could not reach Ollama. Ensure server is active.\n\n")

if __name__ == "__main__":
    app = ArchimedesPro()
    app.mainloop()