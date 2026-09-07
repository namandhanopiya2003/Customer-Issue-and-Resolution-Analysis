-- ============================================================
-- SET 1: BASIC ANALYSIS
-- Purpose: Understand the overall ticket volume, status, issue, product, priority, and channel distribution in the dataset.
-- ============================================================


-- QUERY 1
-- Count the total number of tickets in the cleaned dataset.
SELECT
    COUNT(*) AS total_tickets
FROM customer_tickets;


-- QUERY 2
-- Count tickets by ticket status to understand the overall distribution of open, closed, and pending tickets.
SELECT
    ticket_status,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY ticket_status
ORDER BY ticket_count DESC;


-- QUERY 3
-- Count tickets by ticket type to identify the most common categories of customer issues.
SELECT
    ticket_type,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY ticket_type
ORDER BY ticket_count DESC;


-- QUERY 4
-- Count tickets by product to identify which products generate the highest volume of customer support tickets.
SELECT
    product_purchased,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY product_purchased
ORDER BY ticket_count DESC;


-- QUERY 5
-- Count tickets by priority and channel to understand how support demand is distributed across these dimensions.
SELECT
    ticket_priority,
    ticket_channel,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY ticket_priority, ticket_channel
ORDER BY ticket_count DESC;