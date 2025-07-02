import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Optional, Dict, Any

class FirestoreCRUD:

    def __init__(self, cred_path: str):
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            print("Firestore client initialized successfully")
        except Exception as e:
            print(f"Error initializing Firestore: {e}")
            raise

    def create_document(self, collection_name: str, document_data: Dict[str, Any], document_id: Optional[str] = None) -> str:
        try:
            if document_id:
                doc_ref = self.db.collection(collection_name).document(document_id)
                doc_ref.set(document_data)
            else:
                doc_ref = self.db.collection(collection_name).document()
                doc_ref.set(document_data)
                document_id = doc_ref.id
                
            print(f"Document created with ID: {document_id}")
            return document_id
        except Exception as e:
            print(f"Error creating document: {e}")
            raise

    def read_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc = doc_ref.get()
            
            if doc.exists:
                print(f"Document found: {doc.to_dict()}")
                return doc.to_dict()
            else:
                print(f"No document found with ID: {document_id}")
                return None
        except Exception as e:
            print(f"Error reading document: {e}")
            raise

    def update_document(self, collection_name: str, document_id: str, update_data: Dict[str, Any], merge: bool = True) -> bool:
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.set(update_data, merge=merge)
            print(f"Document {document_id} updated successfully")
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            raise

    def delete_document(self, collection_name: str, document_id: str) -> bool:
        try:
            doc_ref = self.db.collection(collection_name).document(document_id)
            doc_ref.delete()
            print(f"Document {document_id} deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            raise

    def query_collection(self, collection_name: str, query_params: Dict[str, Any], limit: Optional[int] = None) -> list:
        try:
            collection_ref = self.db.collection(collection_name)
            
            # Build the query
            query = collection_ref
            for field, value in query_params.items():
                query = query.where(field, "==", value)
                
            if limit:
                query = query.limit(limit)
                
            results = query.stream()
            
            documents = []
            for doc in results:
                documents.append({"id": doc.id, **doc.to_dict()})
                
            print(f"Found {len(documents)} matching documents")
            return documents
        except Exception as e:
            print(f"Error querying collection: {e}")
            raise

    def list_collection_documents(self, collection_name: str) -> list:
        """
        List all documents in a collection
        
        Args:
            collection_name: Name of the Firestore collection
            
        Returns:
            List of all documents in the collection
        """
        try:
            docs = self.db.collection(collection_name).stream()
            documents = []
            
            for doc in docs:
                documents.append({"id": doc.id, **doc.to_dict()})
                
            print(f"Collection {collection_name} contains {len(documents)} documents")
            return documents
        except Exception as e:
            print(f"Error listing documents: {e}")
            raise


# Example Usage
if __name__ == "__main__":
    # Initialize with your service account JSON path
    firestore_crud = FirestoreCRUD("path/to/your/serviceAccountKey.json")
    
    # Example collection name
    collection = "users"
    
    # Create a document
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "is_active": True
    }
    doc_id = firestore_crud.create_document(collection, user_data)
    
    # Read the document
    user = firestore_crud.read_document(collection, doc_id)
    print(f"Retrieved user: {user}")
    
    # Update the document
    update_data = {
        "age": 31,
        "last_updated": firestore.SERVER_TIMESTAMP
    }
    firestore_crud.update_document(collection, doc_id, update_data)
    
    # Query documents
    query_results = firestore_crud.query_collection(
        collection, 
        {"is_active": True}, 
        limit=5
    )
    print(f"Active users: {query_results}")
    
    # List all documents
    all_users = firestore_crud.list_collection_documents(collection)
    print(f"All users: {all_users}")
    
    # Delete the document
    firestore_crud.delete_document(collection, doc_id)