import json
from enum import Enum

from bson import json_util

from core.database.connection import db
from core.exceptions.profile import ProfileCreateError, ProfileNotFound
from core.middlewares.catch_exceptions import logger


def get_all_candidates():
    profile_collection = db.client["candidate"].users
    candidates_cursor = profile_collection.find()

    # Convert cursor to a list of dictionaries
    candidates = [json.loads(json_util.dumps(doc)) for doc in candidates_cursor]

    return candidates


def create_candidate(request_body):
    candidate_dict = request_body.dict()

    candidate_dict['career_level'] = candidate_dict['career_level'].value
    candidate_dict['gender'] = candidate_dict['gender'].value
    candidate_dict['degree_type'] = candidate_dict['degree_type'].value
    try:
        profile_collection = db.client["candidate"].candidates
        profile_collection.insert_one(candidate_dict)
        return candidate_dict
    except Exception as e:
        logger.error(f"Error: {e}")
        raise ProfileCreateError


def specific_candidate(uuid):
    profile_collection = db.client["candidate"].users
    profile = profile_collection.find_one({"uuid": uuid})

    if profile:
        # Convert the MongoDB document to a JSON string and then parse it back into a dictionary
        profile_json = json.loads(json_util.dumps(profile))
        return profile_json
    else:
        raise ProfileNotFound


def delete_specific_candidate(uuid):
    profile_collection = db.client["candidate"].users
    object_query = profile_collection.find_one({"uuid": uuid})
    if object_query:
        profile_collection.delete_many(object_query)
    else:
        raise ProfileNotFound


def patch_specific_profile(uuid, request_body):
    profile_collection = db.client["candidate"].users

    request_body_dict = request_body.dict()
    print("Request Body Dict:", request_body_dict)  # Debugging

    for key, value in request_body_dict.items():
        if isinstance(value, Enum):
            request_body_dict[key] = value.value

    update_result = profile_collection.update_one(
        {"uuid": uuid},
        {"$set": request_body_dict}
    )

    print("Matched Count:", update_result.matched_count)  # Debugging
    print("Modified Count:", update_result.modified_count)  # Debugging

    if update_result.matched_count == 0:
        return False, "No document found with the provided UUID."

    if update_result.modified_count == 0:
        return False, "Document found but not modified."

    return True, "Document successfully updated."
