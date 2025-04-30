from rest_framework.pagination import PageNumberPagination

class QuestionPagination(PageNumberPagination):
    """Custom pagination settings for questions list"""
    page_size = 10  # Default items per page
    page_size_query_param = 'page_size'  # Allows client to override (e.g., ?page_size=20)
    max_page_size = 100  # Maximum allowed page size