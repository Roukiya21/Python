from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    results = []
    included_ids = set()

    for user in USERS:
        user_id = str(user["id"])


        if "id" in args and args["id"] == user_id:
            results.append((user, "id"))
            included_ids.add(user_id)
            continue


        if "name" in args and args["name"].lower() in user["name"].lower():
            if user_id not in included_ids:
                results.append((user, "name"))
                included_ids.add(user_id)
            continue


        if "age" in args:
            try:
                age = int(args["age"])
                if (user["age"] - 1) <= age <= (user["age"] + 1) and user_id not in included_ids:
                    results.append((user, "age"))
                    included_ids.add(user_id)
            except ValueError:
                pass  


        if "occupation" in args and args["occupation"].lower() in user["occupation"].lower():
            if user_id not in included_ids:
                results.append((user, "occupation"))
                included_ids.add(user_id)


    sorted_results = sorted(results, key=lambda x: ("id", "name", "age", "occupation").index(x[1]))


    sorted_users = [{"id": str(user["id"]), "name": user["name"], "age": user["age"], "occupation": user["occupation"]} for user, _ in sorted_results]

    return sorted_users
