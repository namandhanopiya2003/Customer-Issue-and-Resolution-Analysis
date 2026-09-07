-- ============================================================
-- SET 3: CROSS ANALYSIS
-- Purpose: Analyze relationships between products, issues, priorities, channels, and customer satisfaction to identify patterns that may require further business investigation.
-- ============================================================


-- QUERY 1
-- Identify the most common combinations of product and ticket subject to understand which issues are concentrated within specific products.
SELECT
    product_purchased,
    ticket_subject,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY product_purchased, ticket_subject
ORDER BY ticket_count DESC;


-- QUERY 2
-- Analyze the distribution of ticket priorities within each ticket type.
SELECT
    ticket_type,
    ticket_priority,
    COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY ticket_type, ticket_priority
ORDER BY ticket_type, ticket_count DESC;


-- QUERY 3
-- Analyze ticket priority distribution across support channels.
SELECT
c13,
c14,
COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY c13, c14
ORDER BY ticket_count DESC;


-- QUERY 4
-- Analyze ticket status distribution across ticket priorities.
SELECT
c11,
c13,
COUNT(*) AS ticket_count
FROM customer_tickets
GROUP BY c11, c13
ORDER BY ticket_count DESC;


-- QUERY 5
-- Identify product and ticket subject combinations with high ticket volume and available satisfaction ratings.
SELECT
    product_purchased,
    ticket_subject,
    COUNT(*) AS total_tickets,
    COUNT(customer_satisfaction_rating) AS rated_tickets,
    ROUND(AVG(customer_satisfaction_rating), 2) AS average_satisfaction
FROM customer_tickets
GROUP BY product_purchased, ticket_subject
HAVING COUNT(*) > 0
ORDER BY total_tickets DESC, average_satisfaction ASC;