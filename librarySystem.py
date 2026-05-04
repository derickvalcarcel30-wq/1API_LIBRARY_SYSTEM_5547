
import asyncio
import datetime
from typing import List, Dict, Optional, Union, Tuple, Any


library_name: str = "Limkokwing University Library"
max_loan_days: int = 24
daily_fine_rate: float = 10000.0
is_operational: bool = True

book_categories: List[str] = ["Technology", "Literature", "History", "Science"]
library_coordinates: Tuple[float, float] = (8.4844, -13.2344)
temporary_message: Union[str, None] = None


class Book:
    """Book model with full type annotations"""
    
    def __init__(self, book_id: int, title: str, author: str, category: str, available_copies: int) -> None:
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.category: str = category
        self.available_copies: int = available_copies
    
    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available_copies": self.available_copies
        }


class BorrowRecord:
    """Borrow transaction record"""
    
    def __init__(self, borrow_id: int, user_id: int, user_name: str, book_id: int, 
                 book_title: str, borrow_date: str) -> None:
        self.borrow_id: int = borrow_id
        self.user_id: int = user_id
        self.user_name: str = user_name
        self.book_id: int = book_id
        self.book_title: str = book_title
        self.borrow_date: str = borrow_date
        self.return_date: Optional[str] = None
        self.status: str = "borrowed"
        self.fine: int = 0
    
    def to_dict(self) -> Dict[str, Union[str, int, None]]:
        return {
            "borrow_id": self.borrow_id,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "book_title": self.book_title,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "status": self.status,
            "fine": self.fine
        }


class User:
    """Library user model"""
    
    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id: int = user_id
        self.name: str = name
        self.email: str = email
        self.borrowed_books: List[int] = []



class LibraryDatabase:
    """Manages all library data"""
    
    def __init__(self) -> None:
        self.books: Dict[int, Book] = {}
        self.borrow_records: Dict[int, BorrowRecord] = {}
        self.users: Dict[int, User] = {}
        self.next_borrow_id: int = 5001
        self._initialize_data()
    
    def _initialize_data(self) -> None:
        """Initialize with sample data"""
        
        books_data: List[Tuple[int, str, str, str, int]] = [
            (101, "Python Programming", "Lucifer Morningstar", "Technology", 3),
            (102, "Introduction To Software Enginnering", "Derick Valcarcel", "Technology", 2),
            (103, "How To Steal From Your Parents", "Derick Valcarcel", "Literature", 4),
            (104, "Sierra Leone History", "John Karefa", "History", 2),
            (105, "Web Development with React", "Bob Wilson", "Technology", 1),
            (106, "African Poetry Collection", "Maya Angelou", "Literature", 3),
            (107, "The Road To Heaven", "Derick Valcarcel", "Science", 2),
            (108, "Database Design Fundamentals", "Michael Chen", "Technology", 3),
            (109, "The Beautiful Ones Are Born", "Emmanuel Jal", "Literature", 2),
            (110, "Climate Change in Africa", "Wangari Maathai", "Science", 1),
        ]
        
        for book_data in books_data:
            book_id, title, author, category, copies = book_data
            self.books[book_id] = Book(book_id, title, author, category, copies)
        
        users_data: List[Tuple[int, str, str]] = [
            (5547, "Derick Valcarcel", "Valcarcel@Gmail.com"),
            (5548, "Musa Sesay", "Sesay@Gmail.com"),
            (5549, "Dericksha Valcarcel", "Dericksha@Gmail.com"),
            (5550, "Isha Sesay", "Isha@Gmail.com"),
            (5551, "Emmanuel Kamara", "emmanuel@Gmail.com"),
            (5552, "Fatmata Kargbo", "fatmata@Gmail.com"),
        ]
        
        for user_data in users_data:
            user_id, name, email = user_data
            self.users[user_id] = User(user_id, name, email)
    
    def search_books(self, query: str, search_by: str = "title") -> List[Dict[str, Union[str, int]]]:
        """Search books by title, author, or category"""
        results: List[Dict[str, Union[str, int]]] = []
        query_lower: str = query.lower()
        
        for book in self.books.values():
            match: bool = False
            if search_by == "title" and query_lower in book.title.lower():
                match = True
            elif search_by == "author" and query_lower in book.author.lower():
                match = True
            elif search_by == "category" and query_lower in book.category.lower():
                match = True
            
            if match:
                results.append(book.to_dict())
        
        return results
    
    def borrow_book(self, user_id: int, book_id: int, borrow_date: str) -> Tuple[bool, Union[int, str], str]:
        """Process book borrowing"""
        if user_id not in self.users:
            return False, f"User ID {user_id} not found", ""
        
        if book_id not in self.books:
            return False, f"Book ID {book_id} not found", ""
        
        book: Book = self.books[book_id]
        
        if book.available_copies <= 0:
            return False, f"'{book.title}' is unavailable (0 copies left)", ""
        
        borrow_datetime: datetime.datetime = datetime.datetime.strptime(borrow_date, "%Y-%m-%d")
        due_datetime: datetime.datetime = borrow_datetime + datetime.timedelta(days=max_loan_days)
        due_date: str = due_datetime.strftime("%Y-%m-%d")
        
        borrow_id: int = self.next_borrow_id
        self.next_borrow_id += 1
        
        record: BorrowRecord = BorrowRecord(
            borrow_id=borrow_id,
            user_id=user_id,
            user_name=self.users[user_id].name,
            book_id=book_id,
            book_title=book.title,
            borrow_date=borrow_date
        )
        
        self.borrow_records[borrow_id] = record
        self.users[user_id].borrowed_books.append(book_id)
        self.books[book_id].available_copies -= 1
        
        return True, borrow_id, due_date
    
    def return_book(self, borrow_id: int, return_date: str) -> Tuple[bool, Union[int, str]]:
        """Process book return and calculate fine"""
        if borrow_id not in self.borrow_records:
            return False, f"Borrow record {borrow_id} not found"
        
        record: BorrowRecord = self.borrow_records[borrow_id]
        
        if record.status == "returned":
            return False, "Book already returned"
        
        borrow_datetime: datetime.datetime = datetime.datetime.strptime(record.borrow_date, "%Y-%m-%d")
        due_datetime: datetime.datetime = borrow_datetime + datetime.timedelta(days=max_loan_days)
        return_datetime: datetime.datetime = datetime.datetime.strptime(return_date, "%Y-%m-%d")
        
        fine: int = 0
        if return_datetime > due_datetime:
            days_late: int = (return_datetime - due_datetime).days
            fine = int(days_late * daily_fine_rate)
            record.status = "overdue"
        else:
            record.status = "returned"
        
        record.return_date = return_date
        record.fine = fine
        
        self.books[record.book_id].available_copies += 1
        
        if record.user_id in self.users:
            if record.book_id in self.users[record.user_id].borrowed_books:
                self.users[record.user_id].borrowed_books.remove(record.book_id)
        
        return True, fine
    
    def get_user_history(self, user_id: int) -> List[Dict[str, Union[str, int, None]]]:
        """Get user's borrowing history"""
        history: List[Dict[str, Union[str, int, None]]] = []
        for record in self.borrow_records.values():
            if record.user_id == user_id:
                history.append(record.to_dict())
        return history
    
    def get_all_books(self) -> List[Dict[str, Union[str, int]]]:
        """Get all books"""
        return [book.to_dict() for book in self.books.values()]
    
    def get_user_active_borrows(self, user_id: int) -> List[Dict[str, Union[str, int, None]]]:
        """Get currently borrowed books for a user"""
        active: List[Dict[str, Union[str, int, None]]] = []
        for record in self.borrow_records.values():
            if record.user_id == user_id and record.status == "borrowed":
                active.append(record.to_dict())
        return active


async def async_borrow_book(db: LibraryDatabase, user_id: int, book_id: int, 
                            borrow_date: str, user_name: str) -> Dict[str, Any]:
    """Async function for borrowing a book - non-blocking"""
    print(f"   [ASYNC] {user_name} is borrowing book {book_id}...")
    await asyncio.sleep(0.3)
    success, result, due_date = db.borrow_book(user_id, book_id, borrow_date)
    
    if success:
        return {"success": True, "user": user_name, "borrow_id": result, 
                "due_date": due_date, "message": f"SUCCESS: {user_name} borrowed book {book_id}"}
    else:
        return {"success": False, "user": user_name, "message": f"FAILED: {user_name} - {result}"}


async def async_return_book(db: LibraryDatabase, borrow_id: int, return_date: str) -> Dict[str, Any]:
    """Async function for returning a book"""
    print(f"   [ASYNC] Processing return for borrow ID {borrow_id}...")
    await asyncio.sleep(0.3)
    success, result = db.return_book(borrow_id, return_date)
    
    if success:
        if result > 0:
            return {"success": True, "fine": result, "message": f"LATE RETURN! Fine: {result} Leones"}
        else:
            return {"success": True, "fine": 0, "message": "ON TIME RETURN! No fine."}
    else:
        return {"success": False, "message": f"FAILED: {result}"}


async def demo_concurrent_borrowing() -> None:
    """Demonstrate async concurrent operations"""
    print("\n" + "="*70)
    print("DEMONSTRATION: ASYNCHRONOUS CONCURRENT BORROWING")
    print("="*70)
    print("\nEXPLANATION:")
    print("   Without async: 6 users x 0.3 seconds = 1.8 seconds total")
    print("   WITH async: All 6 users borrow SIMULTANEOUSLY")
    print("   Total time = ~0.3 seconds")
    
    db: LibraryDatabase = LibraryDatabase()
    
    tasks: List = [
        async_borrow_book(db, 5547, 101, "2026-04-30", "Derick"),
        async_borrow_book(db, 5548, 101, "2026-04-30", "Musa"),
        async_borrow_book(db, 5549, 103, "2026-04-30", "Dericksha"),
        async_borrow_book(db, 5550, 105, "2026-04-30", "Isha"),
        async_borrow_book(db, 5551, 107, "2026-04-30", "Emmanuel"),
        async_borrow_book(db, 5552, 108, "2026-04-30", "Fatmata"),
    ]
    
    print("\nStarting ALL 6 requests SIMULTANEOUSLY...\n")
    start_time: datetime.datetime = datetime.datetime.now()
    
    results: List[Dict[str, Any]] = await asyncio.gather(*tasks)
    
    end_time: datetime.datetime = datetime.datetime.now()
    total_time: float = (end_time - start_time).total_seconds()
    
    print("\n" + "-"*50)
    print("RESULTS:")
    print("-"*50)
    for result in results:
        print(f"   {result['message']}")
    
    print(f"\nTotal time for {len(tasks)} concurrent operations: {total_time:.2f} seconds")
    print("\nADVANTAGE OF ASYNC PROGRAMMING:")
    print("   - Multiple users can use the system at the same time")
    print("   - No user has to wait for others to finish")
    print("   - Better efficiency for library with many students")
    print("="*70)


async def demo_async_return_with_fine() -> None:
    """Demonstrate async return with fine calculation"""
    print("\n" + "="*70)
    print("DEMONSTRATION: ASYNC RETURN WITH FINE CALCULATION")
    print("="*70)
    
    db: LibraryDatabase = LibraryDatabase()
    
    print("\nStep 1: Borrow a book (to be returned late)")
    success, borrow_id, due_date = db.borrow_book(1001, 101, "2026-04-01")
    
    if success:
        print(f"   SUCCESS: Book borrowed! Borrow ID: {borrow_id}")
        print(f"   Due date: {due_date}")
        
        print("\nStep 2: Return the book LATE (after due date)")
        result = await async_return_book(db, borrow_id, "2026-04-29")
        
        print(f"\nRESULT:")
        print(f"   {result['message']}")
        if result.get('fine', 0) > 0:
            print(f"   Fine calculation: {result['fine']} Leones")
            print(f"   Late days: 14 days x {int(daily_fine_rate)} Leones/day = {result['fine']} Leones")
    
    print("="*70)


def print_header() -> None:
    """Display application header"""
    print("\n" + "="*70)
    print("   LIMKOKWING UNIVERSITY LIBRARY MANAGEMENT SYSTEM")
    print("   PROG315 - Object Oriented Programming 2")
    print("   " + datetime.datetime.now().strftime("%B %d, %Y"))
    print("="*70)


def print_menu() -> None:
    """Display main menu options"""
    print("\n" + "-"*50)
    print("MAIN MENU")
    print("-"*50)
    print("1. Search Books")
    print("2. Borrow a Book")
    print("3. Return a Book")
    print("4. View User Borrowing History")
    print("5. View All Books")
    print("6. View Currently Borrowed Books")
    print("7. DEMO: Async Concurrent Borrowing (Multiple Users)")
    print("8. DEMO: Async Return with Fine Calculation")
    print("9. Exit")
    print("-"*50)


def search_books_menu(db: LibraryDatabase) -> None:
    """Handle book search"""
    print("\n" + "-"*40)
    print("SEARCH BOOKS")
    print("-"*40)
    print("Search by:")
    print("  1. Title")
    print("  2. Author")
    print("  3. Category")
    
    choice: str = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        search_by = "title"
    elif choice == "2":
        search_by = "author"
    elif choice == "3":
        search_by = "category"
    else:
        print("Invalid choice!")
        return
    
    query: str = input(f"Enter {search_by} to search: ").strip()
    
    if not query:
        print("Search query cannot be empty!")
        return
    
    results = db.search_books(query, search_by)
    
    print(f"\nSEARCH RESULTS for '{query}' in {search_by}:")
    print("-"*40)
    
    if results:
        for book in results:
            print(f"\n   ID: {book['id']}")
            print(f"   Title: {book['title']}")
            print(f"   Author: {book['author']}")
            print(f"   Category: {book['category']}")
            print(f"   Available: {book['available_copies']} copies")
    else:
        print("   No books found matching your search.")


def borrow_book_menu(db: LibraryDatabase) -> None:
    """Handle book borrowing"""
    print("\n" + "-"*40)
    print("BORROW A BOOK")
    print("-"*40)
    
    print("\nAVAILABLE BOOKS:")
    print("-"*35)
    
    available_count = 0
    for book in db.get_all_books():
        if book['available_copies'] > 0:
            print(f"   ID: {book['id']:3d} | {book['title']:30} | Copies: {book['available_copies']}")
            available_count += 1
    
    if available_count == 0:
        print("   No books available!")
        return
    
    try:
        print()
        user_id = int(input("Enter your User ID: "))
        book_id = int(input("Enter Book ID to borrow: "))
        borrow_date = input("Enter borrow date (YYYY-MM-DD) [Press Enter for today]: ").strip()
        
        if not borrow_date:
            borrow_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        success, result, due_date = db.borrow_book(user_id, book_id, borrow_date)
        
        if success:
            print(f"\nSUCCESS! Book borrowed successfully!")
            print(f"   Borrow ID: {result}")
            print(f"   Due Date: {due_date}")
            print(f"   Warning: Return by due date to avoid fines of {int(daily_fine_rate)} Leones/day")
        else:
            print(f"\nFAILED: {result}")
            
    except ValueError:
        print("Invalid input! Please enter numbers for IDs.")


def return_book_menu(db: LibraryDatabase) -> None:
    """Handle book return"""
    print("\n" + "-"*40)
    print("RETURN A BOOK")
    print("-"*40)
    
    try:
        borrow_id = int(input("Enter Borrow ID: "))
        return_date = input("Enter return date (YYYY-MM-DD) [Press Enter for today]: ").strip()
        
        if not return_date:
            return_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        success, result = db.return_book(borrow_id, return_date)
        
        if success:
            if result > 0:
                print(f"\nLATE RETURN! BOOK RETURNED LATE!")
                print(f"   Fine amount: {result} Leones")
                print(f"   Please pay fine at library counter.")
            else:
                print(f"\nON TIME! BOOK RETURNED ON TIME!")
                print(f"   No fine to pay.")
        else:
            print(f"\nFAILED: {result}")
            
    except ValueError:
        print("Invalid input! Please enter a number for Borrow ID.")


def view_history_menu(db: LibraryDatabase) -> None:
    """View user borrowing history"""
    print("\n" + "-"*40)
    print("USER BORROWING HISTORY")
    print("-"*40)
    
    try:
        user_id = int(input("Enter User ID: "))
        
        if user_id not in db.users:
            print(f"User with ID {user_id} not found!")
            return
        
        user = db.users[user_id]
        history = db.get_user_history(user_id)
        
        print(f"\nBorrowing History for: {user.name} (ID: {user_id})")
        print("-"*50)
        
        if history:
            for record in history:
                print(f"\n   Borrow ID: {record['borrow_id']}")
                print(f"   Book: {record['book_title']}")
                print(f"   Borrow Date: {record['borrow_date']}")
                print(f"   Return Date: {record['return_date'] or 'Not returned yet'}")
                print(f"   Status: {str(record['status']).upper()}")
                if record['fine'] and record['fine'] > 0:
                    print(f"   Fine: {record['fine']} Leones")
                print("   " + "-"*35)
        else:
            print("   No borrowing history found.")
            
    except ValueError:
        print("Invalid input! Please enter a number for User ID.")


def view_active_borrows_menu(db: LibraryDatabase) -> None:
    """View currently borrowed books for a user"""
    print("\n" + "-"*40)
    print("CURRENTLY BORROWED BOOKS")
    print("-"*40)
    
    try:
        user_id = int(input("Enter User ID: "))
        
        if user_id not in db.users:
            print(f"User with ID {user_id} not found!")
            return
        
        user = db.users[user_id]
        active = db.get_user_active_borrows(user_id)
        
        print(f"\nBooks currently borrowed by: {user.name}")
        print("-"*45)
        
        if active:
            for record in active:
                print(f"\n   Borrow ID: {record['borrow_id']}")
                print(f"   Book: {record['book_title']}")
                print(f"   Borrow Date: {record['borrow_date']}")
                print(f"   Status: ACTIVE")
        else:
            print("   No books currently borrowed.")
            
    except ValueError:
        print("Invalid input! Please enter a number for User ID.")


def view_all_books_menu(db: LibraryDatabase) -> None:
    """Display all books in library"""
    print("\n" + "-"*40)
    print("COMPLETE LIBRARY CATALOG")
    print("-"*40)
    
    books = db.get_all_books()
    
    categories = {}
    for book in books:
        cat = book['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(book)
    
    for category, cat_books in categories.items():
        print(f"\n[{category.upper()}] ({len(cat_books)} books):")
        print("-"*40)
        for book in cat_books:
            status = "Available" if book['available_copies'] > 0 else "Unavailable"
            print(f"   [{book['id']:3d}] {book['title']}")
            print(f"        by {book['author']}")
            print(f"        {status} ({book['available_copies']} copies)")
            print()


async def main() -> None:
    """Main asynchronous entry point"""
    
    db: LibraryDatabase = LibraryDatabase()
    
    print_header()
    print(f"\nWelcome to the Library Management System!")
    print(f"Late fine rate: {int(daily_fine_rate)} Leones per day")
    print(f"Max loan period: {max_loan_days} days")
    
    while True:
        print_menu()
        
        # FIXED: Removed the incorrect 'strip()' parameter
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            search_books_menu(db)
        elif choice == "2":
            borrow_book_menu(db)
        elif choice == "3":
            return_book_menu(db)
        elif choice == "4":
            view_history_menu(db)
        elif choice == "5":
            view_all_books_menu(db)
        elif choice == "6":
            view_active_borrows_menu(db)
        elif choice == "7":
            await demo_concurrent_borrowing()
        elif choice == "8":
            await demo_async_return_with_fine()
        elif choice == "9":
            print("\nThank you for using Limkokwing Library System!")
            print("Goodbye!\n")
            break
        else:
            print("Invalid choice! Please enter 1-9.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    asyncio.run(main())