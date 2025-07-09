# 📚 Book Exchange Platform

A web application built with **Django** that allows users to buy and sell books.  
It features phone number verification using **Twilio**, search powered by **Pinecone**, and responsive UI with **Tailwind CSS**.

---
## 📷 Screenshots

### 🏠 Landing Page
![Landing Page](book_exchange/books/assets/1.png)

---

### 🔐 Login Page
![View Books Page](book_exchange/books/assets/3.png)

---

### 📚 Home Page
![Home Page](book_exchange/books/assets/2.png)

---

### 🔍 View Books Page
![View Books Page](book_exchange/books/assets/4.png)

---

### ✍️ Sell a Book Page
![Sell a Book](book_exchange/books/assets/5.png)

---

### 📁 Your Books Page
![Your Books](book_exchange/books/assets/6.png)


## 🚀 Features

- 🔐 OTP-based phone number verification using Twilio
- 📖 List, search, edit, and delete books
- 🔍 Semantic search via Pinecone and Cohere embeddings
- 🎨 Clean, responsive design with Tailwind CSS
- 📱 Secure access to seller phone numbers via request system

---

## 🛠️ Tech Stack

- **Backend**: Django
- **Frontend**: Tailwind CSS
- **OTP Service**: Twilio
- **Search Engine**: Pinecone + Cohere Embeddings

---

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file and add:

```
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number
COHERE_API_KEY=your_cohere_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_env
```

4. **Run migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the server**

```bash
python manage.py runserver
```

---


## 📂 Project Structure

- `Auth/` — handles user verification via Twilio
- `books/` — core logic for listing, searching, editing books
- `templates/` — HTML templates
- `static/` — Tailwind assets

---

## 🧠 Semantic Search

Search queries are embedded using Cohere and matched using Pinecone vector index.  
Top results are returned based on semantic relevance.

---

## 🙋‍♂️ Author

Developed by Parth Honkalse

---

## 📄 License

This project is licensed under the MIT License.
EOL
