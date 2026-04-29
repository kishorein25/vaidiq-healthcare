"""
MongoDB Connection Module
Handles async MongoDB connections using Motor driver
Used for storing medical records, images, videos, prescriptions
"""

from motor.motor_asyncio import AsyncClient, AsyncDatabase, AsyncCollection
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client and database
mongodb_client: AsyncClient = None
mongodb_db: AsyncDatabase = None


async def connect_to_mongo():
    """
    Create MongoDB connection on application startup
    Uses Motor for async operations
    """
    global mongodb_client, mongodb_db
    
    try:
        logger.info("🔌 Connecting to MongoDB Atlas...")
        
        mongodb_client = AsyncClient(settings.MONGODB_URL)
        
        # Verify connection
        await mongodb_client.admin.command('ping')
        
        # Set database
        mongodb_db = mongodb_client[settings.MONGODB_DB_NAME]
        
        logger.info(f"✅ Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
        
        # Create indexes for better performance
        await create_mongo_indexes()
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise e


async def close_mongo_connection():
    """
    Close MongoDB connection on application shutdown
    """
    global mongodb_client, mongodb_db
    
    try:
        if mongodb_client:
            mongodb_client.close()
            logger.info("✅ MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {str(e)}")


async def create_mongo_indexes():
    """
    Create indexes for better query performance
    """
    try:
        # Medical Records indexes
        medical_records = mongodb_db["medical_records"]
        await medical_records.create_index("patient_id")
        await medical_records.create_index("doctor_id")
        await medical_records.create_index("created_at")
        
        # Prescriptions indexes
        prescriptions = mongodb_db["prescriptions"]
        await prescriptions.create_index("patient_id")
        await prescriptions.create_index("doctor_id")
        await prescriptions.create_index("prescription_date")
        
        # Medical History indexes
        medical_history = mongodb_db["medical_history"]
        await medical_history.create_index("patient_id")
        await medical_history.create_index([("created_at", -1)])
        
        # Chat History indexes
        chat_history = mongodb_db["chat_history"]
        await chat_history.create_index("user_id")
        await chat_history.create_index("created_at")
        
        logger.info("✅ MongoDB indexes created successfully")
        
    except Exception as e:
        logger.error(f"⚠️ Error creating MongoDB indexes: {str(e)}")


def get_mongodb() -> AsyncDatabase:
    """
    Get MongoDB database instance
    Use in dependency injection
    """
    if mongodb_db is None:
        raise RuntimeError("MongoDB not connected. Call connect_to_mongo() first.")
    return mongodb_db


async def get_mongo_collection(collection_name: str) -> AsyncCollection:
    """
    Get a specific MongoDB collection
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        AsyncCollection instance
    """
    if mongodb_db is None:
        raise RuntimeError("MongoDB not connected. Call connect_to_mongo() first.")
    return mongodb_db[collection_name]


# MongoDB Collections
class MongoCollections:
    """
    Static class to access MongoDB collections
    Usage: await MongoCollections.medical_records().find_one()
    """
    
    @staticmethod
    async def medical_records() -> AsyncCollection:
        return await get_mongo_collection("medical_records")
    
    @staticmethod
    async def prescriptions() -> AsyncCollection:
        return await get_mongo_collection("prescriptions")
    
    @staticmethod
    async def medical_history() -> AsyncCollection:
        return await get_mongo_collection("medical_history")
    
    @staticmethod
    async def chat_history() -> AsyncCollection:
        return await get_mongo_collection("chat_history")
    
    @staticmethod
    async def uploaded_files() -> AsyncCollection:
        return await get_mongo_collection("uploaded_files")
    
    @staticmethod
    async def doctor_documents() -> AsyncCollection:
        return await get_mongo_collection("doctor_documents")


# Helper functions for common operations

async def insert_medical_record(patient_id: int, doctor_id: int, record_data: dict) -> str:
    """
    Insert a medical record
    
    Args:
        patient_id: Patient ID
        doctor_id: Doctor ID
        record_data: Medical record data
        
    Returns:
        Inserted document ID
    """
    collection = await MongoCollections.medical_records()
    record_data["patient_id"] = patient_id
    record_data["doctor_id"] = doctor_id
    
    from datetime import datetime
    record_data["created_at"] = datetime.utcnow()
    
    result = await collection.insert_one(record_data)
    return str(result.inserted_id)


async def get_patient_medical_history(patient_id: int, limit: int = 50) -> list:
    """
    Get all medical records for a patient
    
    Args:
        patient_id: Patient ID
        limit: Number of records to fetch
        
    Returns:
        List of medical records
    """
    collection = await MongoCollections.medical_records()
    records = await collection.find({"patient_id": patient_id}).sort("created_at", -1).limit(limit).to_list(None)
    
    for record in records:
        record["_id"] = str(record["_id"])
    
    return records


async def save_prescription(patient_id: int, doctor_id: int, prescription_data: dict) -> str:
    """
    Save a prescription
    
    Args:
        patient_id: Patient ID
        doctor_id: Doctor ID
        prescription_data: Prescription details
        
    Returns:
        Prescription ID
    """
    collection = await MongoCollections.prescriptions()
    prescription_data["patient_id"] = patient_id
    prescription_data["doctor_id"] = doctor_id
    
    from datetime import datetime
    prescription_data["prescription_date"] = datetime.utcnow()
    
    result = await collection.insert_one(prescription_data)
    return str(result.inserted_id)


async def save_chat_message(user_id: int, message: str, response: str, user_type: str) -> str:
    """
    Save AI chat message for history
    
    Args:
        user_id: User ID
        message: User message
        response: AI response
        user_type: Type of user (patient, doctor, etc.)
        
    Returns:
        Chat message ID
    """
    collection = await MongoCollections.chat_history()
    
    from datetime import datetime
    chat_data = {
        "user_id": user_id,
        "user_type": user_type,
        "message": message,
        "response": response,
        "created_at": datetime.utcnow()
    }
    
    result = await collection.insert_one(chat_data)
    return str(result.inserted_id)
