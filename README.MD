Project Overview

This project is a Library Management System API. It allows users to manage books, register users, and handle borrowing and returning of books.

The system demonstrates Object-Oriented Programming (OOP) principles and asynchronous programming using Python.

Features
Add new books
View all books
Register users
Borrow books
Return books
Asynchronous API endpoints
OOP Concepts Used
Encapsulation: Classes like Book and User store data and behavior
Abstraction: API hides implementation details
Modularity: Code split into models, database, and main API
Technologies Used
Python
FastAPI
Project Structure
library_api/
│── main.py
│── models.py
│── database.py
│── README.md

🔗 API Endpoints
Method	Endpoint	Description
POST	/books/	Add a book
GET	/books/	Get all books
POST	/users/	Register user
POST	/borrow/	Borrow book
POST	/return/	Return book
SDG Alignment

This project supports Quality Education (SDG 4) by improving access to library resources through digital systems.

Challenges Faced
Understanding asynchronous functions
Managing data without a real database
Structuring API endpoints properly
Future Improvements
Add database (MySQL or PostgreSQL)
User authentication system
Book search functionality
Frontend interface

Author
Derick Samuel Valcarcel

