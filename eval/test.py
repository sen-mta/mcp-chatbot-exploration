from server import retrieve_relevant_content, submit_ticket

hasil = retrieve_relevant_content("ac bocor diapain ya?", "engineering")
print(hasil)

# import time
# from server import retrieve_relevant_content, submit_ticket  # Assuming this import works


# def test_query_processing(queries):
#     """
#     Tests the query processing time for a list of queries.

#     Args:
#         queries: A list of tuples, where each tuple contains (query_string, department).

#     Returns:
#         A dictionary containing processing times for each query and the average processing time.
#     """

#     results = {}
#     total_processing_time = 0

#     for query, department in queries:
#         start_time = time.time()
#         try:
#             retrieve_relevant_content(query, department) 
#             # You might want to assert something about 'hasil' here 
#             # to make this a real test (e.g., assert hasil is not None)
#             end_time = time.time()
#             processing_time = end_time - start_time
#             results[(query, department)] = processing_time
#             total_processing_time += processing_time
#         except Exception as e:  # Handle potential errors during processing
#             results[(query, department)] = f"Error: {e}"  # Record the error

#     average_processing_time = total_processing_time / len(queries) if len(queries) > 0 else 0

#     return results, average_processing_time


# queries = [
#     # Restaurant Team
#     ("Is there a gluten-free menu?", "restaurant"),
#     ("Do you have any vegetarian/vegan options?", "restaurant"),
#     ("What time does the restaurant close?", "restaurant"),
#     ("Can I make a reservation for tonight?", "restaurant"),
#     ("Do you offer room service?", "restaurant"),
#     ("Is there a dress code?", "restaurant"),
#     ("Can I see a wine list?", "restaurant"),
#     ("Do you have high chairs for babies?", "restaurant"),
#     ("Is there a children's menu?", "restaurant"),
#     ("Can I get this dish made without [ingredient]?", "restaurant"),
#     ("What is the Wi-Fi password?", "restaurant"),
#     ("Is there outdoor seating?", "restaurant"),
#     ("Can I order takeout?", "restaurant"),
#     ("Do you cater events?", "restaurant"),
#     ("Is there a breakfast buffet?", "restaurant"),
#     ("What time is breakfast served?", "restaurant"),
#     ("Can I get a coffee to go?", "restaurant"),
#     ("Do you have any local beers on tap?", "restaurant"),


#     # Engineering Team (Guests rarely directly interact with engineering but might report issues)
#     ("The air conditioning in my room isn't working.", "engineering"),
#     ("The TV in my room doesn't have any signal.", "engineering"),
#     ("The toilet is clogged.", "engineering"),
#     ("There's no hot water in the shower.", "engineering"),
#     ("The lights in my room are flickering.", "engineering"),
#     ("The Wi-Fi isn't working in my room.", "engineering"),
#     ("I can't seem to get the safe to lock.", "engineering"),
#     ("The phone in my room is dead.", "engineering"),
#     ("There's a leak in the ceiling.", "engineering"),
#     ("The elevator is stuck.", "engineering"),


#     # Housekeeping Team
#     ("Can I get extra towels?", "housekeeping"),
#     ("Can I get my room cleaned now?", "housekeeping"),
#     ("Can I have extra pillows?", "housekeeping"),
#     ("Can you provide a wake-up call?", "housekeeping"), 
#     ("Can I have more shampoo/conditioner?", "housekeeping"),
#     ("My room hasn't been cleaned yet.", "housekeeping"),
#     ("I need more coffee pods for the coffee maker.", "housekeeping"),
#     ("Can someone bring up an iron and ironing board?", "housekeeping"),
#     ("Is there a laundry service?", "housekeeping"),
#     ("What time is check-out?", "housekeeping"), 
#     ("Can I have a late check-out?", "housekeeping"), 
#     ("I've lost my room key.", "housekeeping"), 
#     ("Can I get a different room?", "housekeeping"), 
#     ("Is there a crib available?", "housekeeping"),
# ]

# processing_times, average_time = test_query_processing(queries)

# # Print the results in a clear format
# print("Query Processing Times:")
# for query, time_taken in processing_times.items():
#     print(f"  {query[0]} ({query[1]}): {time_taken:.4f} seconds")  # Format to 4 decimal places

# print(f"\nAverage Processing Time: {average_time:.4f} seconds")

