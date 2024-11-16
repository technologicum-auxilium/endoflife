def render_product_summarized(data):
    summarized_data = []
    for item in data:
        if isinstance(item, dict) and "eol" in item:
            summarized_data.append(
                {
                    "eol": item["eol"],
                }
            )
    return summarized_data


def render_product_data(data):
    return data
