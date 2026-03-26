def paginate_page_based(data, request):
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("pageSize", 5))

    total_items = len(data)
    total_pages = (total_items + page_size - 1) // page_size
    start = (page - 1) * page_size
    end = start + page_size

    result = data[start:end]

    metadata = {
        "paginationType": "page-based",
        "page": page,
        "pageSize": page_size,
        "totalItems": total_items,
        "totalPages": total_pages
    }

    return result, metadata