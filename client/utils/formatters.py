from datetime import datetime, date
from typing import List, Dict, Any, Optional
import re
from constants.ui_constants import UIConstants


def format_date(date_str: str, format_type: str = "datetime") -> str:
    if not date_str:
        return "Unknown"

    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(date_str)

        if format_type == "date":
            return dt.strftime(UIConstants.DATE_FORMAT)
        elif format_type == "time":
            return dt.strftime(UIConstants.TIME_FORMAT)
        elif format_type == "datetime":
            return dt.strftime(UIConstants.DATETIME_FORMAT)
        else:
            return dt.strftime(UIConstants.DATETIME_FORMAT)

    except ValueError:
        return "Invalid date"


def format_article_list(
    articles: List[Dict[str, Any]], max_items: Optional[int] = None
) -> str:
    if not articles:
        return "No articles found."

    if max_items is None:
        max_items = UIConstants.ITEMS_PER_PAGE

    formatted_articles = []
    display_count = min(len(articles), max_items)

    for i, article in enumerate(articles[:display_count], 1):
        title = UIConstants.truncate_text(
            article.get("title", "No title"), UIConstants.MAX_TITLE_LENGTH
        )
        article_id = article.get("id", "Unknown")

        formatted_article = f"{i}. {UIConstants.ARTICLE_ID_PREFIX} {article_id}\n   {UIConstants.ARTICLE_TITLE_PREFIX} {title}"
        formatted_articles.append(formatted_article)

    result = "\n".join(formatted_articles)

    if len(articles) > max_items:
        result += f"\n... and {len(articles) - max_items} more articles"

    return result


def format_article_details(article: Dict[str, Any]) -> str:
    if not article:
        return "Article not found."

    lines = []

    title = article.get("title", "No title")
    lines.append(f"{UIConstants.ARTICLE_TITLE_PREFIX} {title}")

    content = article.get("content")
    if content:
        preview = UIConstants.truncate_text(content, UIConstants.MAX_CONTENT_PREVIEW)
        lines.append(f"{UIConstants.ARTICLE_CONTENT_PREFIX} {preview}")

    url = article.get("url")
    if url:
        lines.append(f"{UIConstants.ARTICLE_URL_PREFIX} {url}")

    category = article.get("category")
    if category:
        lines.append(f"Category: {category}")

    published_at = article.get("published_at")
    if published_at:
        formatted_date = format_date(published_at, "date")
        lines.append(f"Published: {formatted_date}")

    lines.append(UIConstants.ARTICLE_SEPARATOR)

    return "\n".join(lines)


def format_server_status(servers: List[Dict[str, Any]]) -> str:
    if not servers:
        return "No servers found."

    formatted_servers = []

    for server in servers:
        name = server.get("name", "Unknown")
        is_active = server.get("is_active", False)
        status = UIConstants.STATUS_ACTIVE if is_active else UIConstants.STATUS_INACTIVE

        last_accessed = server.get("last_accessed")
        if last_accessed:
            formatted_date = format_date(last_accessed, "datetime")
        else:
            formatted_date = "Never"

        server_line = f"{UIConstants.SERVER_NAME_PREFIX} {name}: {status} {UIConstants.SERVER_STATUS_SEPARATOR} {UIConstants.SERVER_LAST_ACCESSED_PREFIX} {formatted_date}"
        formatted_servers.append(server_line)

    return "\n".join(formatted_servers)


def format_notification_list(notifications: List[Dict[str, Any]]) -> str:
    if not notifications:
        return "No notifications found."

    formatted_notifications = []

    for notification in notifications:
        message = notification.get("message", "No message")
        created_at = notification.get("created_at")

        if created_at:
            formatted_date = format_date(created_at, "datetime")
            date_prefix = UIConstants.NOTIFICATION_DATE_FORMAT.format(
                date=formatted_date
            )
        else:
            date_prefix = "[Unknown date]"

        notification_line = f"{UIConstants.NOTIFICATION_PREFIX} {date_prefix} {message}"
        formatted_notifications.append(notification_line)

    return "\n".join(formatted_notifications)


def format_category_list(categories: List[Dict[str, Any]]) -> str:
    if not categories:
        return "No categories found."

    formatted_categories = []

    for i, category in enumerate(categories, 1):
        name = category.get("name", "Unknown")
        is_active = category.get("is_active", True)
        status = UIConstants.STATUS_ACTIVE if is_active else UIConstants.STATUS_INACTIVE

        category_line = f"{i}. {name} - {status}"
        formatted_categories.append(category_line)

    return "\n".join(formatted_categories)


def format_search_results(articles: List[Dict[str, Any]], query: str) -> str:
    if not articles:
        return f"No articles found matching '{query}'."

    header = f"Search Results for '{query}' ({len(articles)} articles found):"
    formatted_articles = format_article_list(articles)

    return f"{header}\n{formatted_articles}"


def format_pagination_info(pagination: Dict[str, Any]) -> str:
    if not pagination:
        return ""

    page = pagination.get("page", 1)
    per_page = pagination.get("per_page", 10)
    total = pagination.get("total", 0)
    total_pages = pagination.get("total_pages", 1)

    return f"Page {page} of {total_pages} (showing {per_page} of {total} items)"


def format_error_summary(errors: List[str]) -> str:
    if not errors:
        return ""

    if len(errors) == 1:
        return f"Error: {errors[0]}"

    header = f"Multiple errors occurred ({len(errors)}):"
    error_list = "\n".join(f"• {error}" for error in errors)

    return f"{header}\n{error_list}"


def format_table(data: List[Dict[str, Any]], headers: List[str]) -> str:
    if not data or not headers:
        return "No data to display."

    col_widths = {}
    for header in headers:
        col_widths[header] = len(header)

    for row in data:
        for header in headers:
            value = str(row.get(header, ""))
            col_widths[header] = max(col_widths[header], len(value))

    separator = "+" + "+".join("-" * (width + 2) for width in col_widths.values()) + "+"

    header_row = (
        "|" + "|".join(f" {header:<{col_widths[header]}} " for header in headers) + "|"
    )

    data_rows = []
    for row in data:
        data_row = (
            "|"
            + "|".join(
                f" {str(row.get(header, '')):<{col_widths[header]}} "
                for header in headers
            )
            + "|"
        )
        data_rows.append(data_row)

    table_parts = [separator, header_row, separator] + data_rows + [separator]

    return "\n".join(table_parts)


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def format_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"
