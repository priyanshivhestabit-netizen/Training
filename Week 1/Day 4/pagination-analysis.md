```
# Pagination Using Link Headers (GitHub API)

## Overview
GitHub REST APIs use pagination to limit the number of results returned per request. Pagination information is provided through the HTTP `Link` response header.

## Link Header
The `Link` header contains URLs for navigating between pages of results.

Example:
```
link: <https://api.github.com/users/octocat/repos?page=2&per_page=5>; rel="next",
      <https://api.github.com/users/octocat/repos?page=10&per_page=5>; rel="last"
```

### Link Relations
- **rel="next"** – URL of the next page  
- **rel="prev"** – URL of the previous page (if available)  
- **rel="first"** – URL of the first page  
- **rel="last"** – URL of the last page  

## Navigating Pages Using Link Headers
Pagination should be handled by following the URLs provided in the `Link` header instead of manually calculating page numbers.

### Example: Fetch Next Page
```bash
curl https://api.github.com/users/octocat/repos?page=2&per_page=5
```

### Example: Fetch Last Page
```bash
curl https://api.github.com/users/octocat/repos?page=10&per_page=5
```

Each response includes a new `Link` header that can be used to continue navigation.

## Benefits
- Prevents incorrect page calculations  
- Adapts automatically to data size changes  
- Ensures reliable and efficient pagination  

## Conclusion
The `Link` header provides a standardized and efficient way to navigate paginated GitHub API responses.
```
