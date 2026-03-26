def paginate_cursor(data, request):
    cursor = request.args.get("cursor", type=int)
    limit = int(request.args.get("limit", 5))

    sorted_data = sorted(data, key=lambda x: x["id"])

    if cursor is None:
        result = sorted_data[:limit]
    else:
        result = [item for item in sorted_data if item["id"] > cursor][:limit]

    next_cursor = result[-1]["id"] if result else None

    metadata = {
        "paginationType": "cursor",
        "cursor": cursor,
        "limit": limit,
        "nextCursor": next_cursor,
        "hasNext": next_cursor is not None and any(item["id"] > next_cursor for item in sorted_data)
    }

    return result, metadata