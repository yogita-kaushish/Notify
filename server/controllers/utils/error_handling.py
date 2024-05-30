def handle_404(e):
    return {
        "error": "Invalid Request URL"
    }

def handle_405(e):
    return {
        "error": "Invalid Request Method"
    }