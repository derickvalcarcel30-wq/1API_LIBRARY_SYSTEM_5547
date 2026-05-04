
import asyncio
import datetime
from typing import Dict, List, Tuple, Union


# ============== TYPE ANNOTATIONS ==============

library_name: str = "Limkokwing Library"
fine_per_day: int = 1000
loan_days: int = 14

books: Dict[int, Dict[str, Union[str, int]]] = {
    101: {"title": "Python Programming", "author": "Lucifer Morningstar", "copies": 3},
    102: {"title": "Introduction To Software Enginnering", "author": "Derick Valcarcel", "copies": 4},
    105: {"title": "Web Development", "author": "Bob Wilson", "copies": 2},
}

borrow_records: Dict[int, Dict[str, Union[int, str]]] = {}
next_borrow_id: int = 5001


# ============== ENDPOINT 1: Borrow a Book ==============

async def borrow_book(user_id: int, book_id: int, borrow_date: str) -> Dict[str, Union[str, int]]:
   

    print(f"   [ASYNC] User {user_id} is trying to borrow book {book_id}...")
    
    await asyncio.sleep(0.5)
    

    if book_id not in books:
        return {"success": 0, "message": f"Book {book_id} not found"}
    
    if books[book_id]["copies"] <= 0:
        return {"success": 0, "message": f"'{books[book_id]['title']}' is not available"}
    

    global next_borrow_id
    borrow_dt = datetime.datetime.strptime(borrow_date, "%Y-%m-%d")
    due_dt = borrow_dt + datetime.timedelta(days=loan_days)
    
    borrow_id = next_borrow_id
    next_borrow_id += 1
    
    borrow_records[borrow_id] = {
        "user_id": user_id,
        "book_id": book_id,
        "book_title": books[book_id]["title"],
        "borrow_date": borrow_date,
        "due_date": due_dt.strftime("%Y-%m-%d"),
        "returned": 0
    }
    

    books[book_id]["copies"] = books[book_id]["copies"] - 1
    
    return {
        "success": 1,
        "borrow_id": borrow_id,
        "book_title": books[book_id]["title"],
        "due_date": due_dt.strftime("%Y-%m-%d"),
        "message": f"SUCCESS: Borrowed '{books[book_id]['title']}'"
    }


# ============== ENDPOINT 2: Return a Book ==============

async def return_book(borrow_id: int, return_date: str) -> Dict[str, Union[str, int]]:

    print(f"   [ASYNC] Processing return for borrow ID {borrow_id}...")
    

    await asyncio.sleep(0.5)
    
    if borrow_id not in borrow_records:
        return {"success": 0, "message": f"Borrow record {borrow_id} not found"}
    
    record = borrow_records[borrow_id]
    
    if record["returned"] == 1:
        return {"success": 0, "message": "Book already returned"}
    
    due_date = datetime.datetime.strptime(record["due_date"], "%Y-%m-%d")
    return_dt = datetime.datetime.strptime(return_date, "%Y-%m-%d")
    
    fine = 0
    if return_dt > due_date:
        days_late = (return_dt - due_date).days
        fine = days_late * fine_per_day

    record["returned"] = 1
    record["return_date"] = return_date
    record["fine"] = fine
    
    book_id = record["book_id"]
    books[book_id]["copies"] = books[book_id]["copies"] + 1
    
    if fine > 0:
        return {
            "success": 1,
            "fine": fine,
            "message": f"LATE RETURN! Fine: {fine} Leones"
        }
    else:
        return {
            "success": 1,
            "fine": 0,
            "message": "ON TIME RETURN! No fine"
        }


# ============== DEMO: Multiple Users Borrowing at SAME Time ==============

async def demo_multiple_users_borrowing():
   
    
    
    # Create 5 borrowing tasks that will run TOGETHER
    tasks = [
        borrow_book(5547, 101, "2026-04-30"),  
        borrow_book(5548, 102, "2026-04-30"),  
        borrow_book(5549, 101, "2026-04-30"),  
        borrow_book(5550, 103, "2026-04-30"),  
        borrow_book(5551, 101, "2026-04-30"),  
    ]
    
    start_time = datetime.datetime.now()
    
    # Run ALL tasks at the SAME time - THIS IS THE MAGIC OF ASYNC!
    results = await asyncio.gather(*tasks)
    
    end_time = datetime.datetime.now()
    total_time = (end_time - start_time).total_seconds()
    
    print("-"*50)
    for result in results:
        print(f"   {result['message']}")
    
    print(f"\nTIME TAKEN: {total_time:.2f} seconds")
    print("\n" + "="*70)



# ============== DEMO: Return with Fine Calculation ==============

async def demo_return_with_fine():
    """Demo showing return endpoint with fine calculation"""
    print("\n" + "="*70)
    print("DEMO: Return a Book with Fine Calculation")
    print("="*70)
    
    
    print("\nSTEP 1: Borrow a book")
    result = await borrow_book(1001, 101, "2026-04-01")
    
    if result["success"] == 1:
        borrow_id = result["borrow_id"]
        print(f"   Borrow ID: {borrow_id}")
        print(f"   Due Date: {result['due_date']}")
        

        print("\nSTEP 2: Return the book LATE")
        return_result = await return_book(borrow_id, "2026-05-15")
        
        print(f"\nRESULT:")
        print(f"   {return_result['message']}")
        if return_result.get("fine", 0) > 0:
            print(f"   Fine amount: {return_result['fine']} Leones")
    
    print("\n" + "="*70)


# ============== MAIN FUNCTION ==============

async def main():
 
    print("\nThe 2 Endpoints in this API:")
    print("   1. borrow_book() - Allows users to borrow books")
    print("   2. return_book() - Allows users to return books")
    
    print("\n" + "-"*50)
    print("RUNNING DEMO 1:")
    print("-"*50)
    await demo_multiple_users_borrowing()
    
    print("\n" + "-"*50)
    print("RUNNING DEMO 2: Return with fine calculation")
    print("-"*50)
    await demo_return_with_fine()
    


if __name__ == "__main__":
    asyncio.run(main())