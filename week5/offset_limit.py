def paginate_offset_limit(data, request):
    offset = int(request.args.get("offset", 0))
    limit = int(request.args.get("limit", 5))

    result = data[offset:offset + limit]

    metadata = {
        "paginationType": "offset-limit",
        "offset": offset,
        "limit": limit,
        "totalItems": len(data),
        "hasNext": offset + limit < len(data)
    }

    return result, metadata