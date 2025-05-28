import logging
import requests
import time
# import uuid
# from datetime import datetime, timezone
from typing import Dict, Any, Optional, Literal
from mcp.server.fastmcp import FastMCP
# import json
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
ticketing_api_base_url = os.getenv("TICKETING_API_BASE_URL")
cloud_run_api_key = os.getenv("CLOUD_RUN_API_KEY")

VALID_GROUPS = ["restoran", "housekeeping", "engineering"]

mcp = FastMCP("hello", host="0.0.0.0", port=8050)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@mcp.tool()
def retrieve_relevant_content(
    query: str, 
    group: Literal["restaurant", "housekeeping", "engineering"]
) -> Dict[str, Any]:
    """
    Retrieves relevant content to answer user questions using RAG (Retrieval-Augmented Generation).
    
    Args:
        query (str): The user question for which relevant content should be retrieved.
        group (Literal["restaurant", "housekeeping", "engineering"]): The content group/category to search within.
            Must be one of: "restaurant", "housekeeping", "engineering".
            
    Returns:
        Dict[str, Any]: Retrieved content relevant to the query, or error information if the request fails.
        
    Raises:
        ValueError: If group is not one of the allowed values.
    """
    start_time = time.time()
    # Log initial request
    logger.info(f"RAG Content Retrieval - Query: '{query}', Group: '{group}'")
    
    # Validate group parameter
    allowed_groups = ["restaurant", "housekeeping", "engineering"]
    if group not in allowed_groups:
        error_msg = f"Group must be one of {allowed_groups}, got: {group}"
        logger.error(f"Validation failed - {error_msg}")
        raise ValueError(error_msg)
    
    url = "https://chatbot-rag-retrieve-related-content-893090234023.us-central1.run.app"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": cloud_run_api_key
    }

    data = {
        "query": query,
        "metadata_filter": {
            "group": group
        },
        "top_k": 2,
        "similarity_threshold": 0.1,
        "with_relations": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        
        result = response.json()
        logger.info(f"Success - Retrieved {group} content for query")
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Time taken for retrieve_relevant_content: {elapsed_time:.4f} seconds")
        return result
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {e}"
        logger.error(f"HTTP Error - Status: {response.status_code}")
        return {"error": error_msg, "status_code": response.status_code}
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        logger.error("Request Error - Failed to connect to RAG service")
        return {"error": error_msg}
        
    except ValueError as e:
        error_msg = f"Failed to parse JSON response: {e}"
        logger.error("Parse Error - Invalid JSON response")
        return {"error": error_msg}

@mcp.tool()
def retrieve_content_by_chunk_index(
    document_id: str, 
    start_index: Optional[int] = None,
    end_index: Optional[int] = None,
    chunk_index: int = 0
) -> Dict[str, Any]:
    """
    Retrieves relevant content by chunk index from a specific document.
    
    Args:
        document_id (str): The ID of the document to retrieve content from.
        start_index (Optional[int]): Starting chunk index. If None, will be calculated based on chunk_index.
        end_index (Optional[int]): Ending chunk index. If None, will be calculated based on chunk_index.
        chunk_index (int): Current chunk index to center the retrieval around. Defaults to 0.
            
    Returns:
        Dict[str, Any]: Retrieved content chunks, or error information if the request fails.
    """
    # Calculate start and end indices if not provided
    if start_index is None or end_index is None:
        start_index = max(0, chunk_index - 3)  # Ensure start_index is not negative
        end_index = chunk_index + 3
    
    # Log initial request
    logger.info(f"Chunk Retrieval - Document: '{document_id}', Chunks: {start_index}-{end_index}")
    
    url = "https://chatbot-rag-retrieve-by-chunk-indexes-893090234023.us-central1.run.app"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": cloud_run_api_key
    }

    data = {
        "document_id": document_id,
        "start_index": start_index,
        "end_index": end_index,
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        
        result = response.json()
        logger.info(f"Success - Retrieved chunks from document '{document_id}'")
        return result
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {e}"
        logger.error(f"HTTP Error - Status: {response.status_code}")
        return {"error": error_msg, "status_code": response.status_code}
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {e}"
        logger.error("Request Error - Failed to connect to chunk service")
        return {"error": error_msg}
        
    except ValueError as e:
        error_msg = f"Failed to parse JSON response: {e}"
        logger.error("Parse Error - Invalid JSON response")
        return {"error": error_msg}

@mcp.tool() 
def submit_ticket(
    group: Literal["restoran", "housekeeping", "engineering"], 
    notes: str,
    room_number: int,
    customer_name: str
) -> str:
    """Submits a new problem ticket to the specified division.

    Args:
        group: The target division for the ticket.
               Must be one of the configured in "restaurant", "housekeeping", "engineering".
        notes: A detailed description of the problem or request. Cannot be empty.
        room_number: The room number associated with the ticket.
        customer_name: The name of the customer reporting the issue. Cannot be empty.

    Returns:
        A confirmation message string if successful.

    Raises:
        ValueError: If input validation fails.
        requests.exceptions.HTTPError: If the ticketing API returns an HTTP error status.
        requests.exceptions.RequestException: For other network/request related issues.
        KeyError: If the API response is missing expected fields.
    """
    # Log initial request (briefly)
    logger.info(
        f"Ticket Submission Attempt - Group: '{group}', Customer: '{customer_name}', "
        f"Room: '{room_number}', Notes: '{notes[:50]}{'...' if len(notes) > 50 else ''}'"
    )

    # --- Input Validation ---
    if group not in VALID_GROUPS:
        error_msg = f"Invalid group '{group}'. Must be one of {VALID_GROUPS}."
        logger.error(f"Validation Error: {error_msg}")
        raise ValueError(error_msg)

    if not notes or not notes.strip():
        error_msg = "Notes cannot be empty or contain only whitespace."
        logger.error(f"Validation Error: {error_msg}")
        raise ValueError(error_msg)

    if not customer_name or not customer_name.strip():
        error_msg = "Customer name cannot be empty or contain only whitespace."
        logger.error(f"Validation Error: {error_msg}")
        raise ValueError(error_msg)

    if room_number <= 0:
        error_msg = f"Invalid room number '{room_number}'. Must be a positive integer."
        logger.error(f"Validation Error: {error_msg}")
        raise ValueError(error_msg)

    # --- API Call ---
    ticketing_endpoint_url = f"{ticketing_api_base_url}/{group}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "room_number": str(room_number),
        "customer_name": customer_name,
        "notes": notes
    }
    print(payload)

    try:
        response = requests.post(
            url = ticketing_endpoint_url,
            headers = headers,
            json=payload
        )
        response.raise_for_status()  

        api_response_data = response.json()

    except Exception as e:
        logger.error(e)
        raise

    try:
        ticket_id = api_response_data['ticketing_id'] 
        status = api_response_data['status']
        # message = api_response_data['message']
    except KeyError as key_err:
        logger.error(
            f"API response from {ticketing_endpoint_url} is missing expected key: {key_err}. "
            f"Response data: {api_response_data}"
        )
        raise KeyError(f"Ticketing API response did not contain expected field: {key_err}")

    confirmation_message = (
        f"Ticket {ticket_id} submitted to {group} division for notes "
        f"'{notes[:30]}{'...' if len(notes) > 30 else ''}' is {status}."
    )
    logger.info(f"Ticket Submission Success: {confirmation_message}")
    return confirmation_message

# Run the server
if __name__ == "__main__":
    mcp.run(transport = "sse")
