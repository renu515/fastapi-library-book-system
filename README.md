# fastapi-library-book-system


##  Project Overview

This project is a backend system built using FastAPI to manage a library system. It includes features like book management, borrowing system, queue handling, and advanced APIs.

##  Features Implemented

* GET APIs (Home, List, Get by ID, Summary)
* POST APIs with Pydantic validation
* CRUD Operations (Create, Update, Delete)
* Helper Functions
* Multi-step Workflow (Borrow, Return, Queue)
* Search functionality
* Sorting functionality
* Pagination
* Combined browsing endpoint

##  How to Run the Project

1. Install dependencies:
   pip install -r requirements.txt

2. Run the server:
   uvicorn main:app --reload

3. Open in browser:
   http://127.0.0.1:8000/docs

##  Screenshots

All API endpoints are tested using Swagger UI and screenshots are included in the screenshots folder.

##  Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
