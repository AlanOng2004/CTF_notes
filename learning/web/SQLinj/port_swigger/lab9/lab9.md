# Lab: Visible error-based SQL injection

This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called users, with columns called username and password. To solve the lab, find a way to leak the password for the administrator user, then log in to their account.

## Conceptual Review

### Extracting sensitive data via verbose SQL error messages

Misconfiguration of the database will sometimes result in verbose error messages. For example, consider the following error message, which occurs after injecting a single quote into an `id` parameter:

> Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char


