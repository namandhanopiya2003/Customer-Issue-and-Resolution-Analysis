-- ============================================================
-- SET 2: PERFORMANCE ANALYSIS
-- Purpose: Analyze resolution availability, first-response records, recorded response-to-resolution intervals, and customer satisfaction.
-- ============================================================


-- QUERY 1
-- Check the availability of resolution information across different ticket statuses.
SELECT
    ticket_status,
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN resolution_available = 1 THEN 1 ELSE 0 END) AS tickets_with_resolution,
    SUM(CASE WHEN resolution_available = 0 THEN 1 ELSE 0 END) AS tickets_without_resolution
FROM customer_tickets
GROUP BY ticket_status
ORDER BY total_tickets DESC;


-- QUERY 2
-- Check the availability of first-response timestamps across different ticket priorities.
SELECT
    ticket_priority,
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN first_response_time IS NOT NULL THEN 1 ELSE 0 END) AS tickets_with_first_response,
    SUM(CASE WHEN first_response_time IS NULL THEN 1 ELSE 0 END) AS tickets_without_first_response
FROM customer_tickets
GROUP BY ticket_priority
ORDER BY total_tickets DESC;


-- QUERY 3
-- Calculate the hours between the recorded first-response timestamp and recorded resolution timestamp.
SELECT
    ticket_id,
    ticket_priority,
    first_response_time,
    time_to_resolution,
    ROUND(
        (julianday(time_to_resolution) - julianday(first_response_time)) * 24,
        2
    ) AS hours_between_response_and_resolution
FROM customer_tickets
WHERE first_response_time IS NOT NULL
  AND time_to_resolution IS NOT NULL
  AND julianday(time_to_resolution) >= julianday(first_response_time)
ORDER BY hours_between_response_and_resolution DESC;


-- QUERY 4
-- Compare the average recorded response-to-resolution interval across ticket priorities.
SELECT
    ticket_priority,
    COUNT(*) AS tickets_with_both_timestamps,
    ROUND(
        AVG(
            (julianday(time_to_resolution) - julianday(first_response_time)) * 24
        ),
        2
    ) AS avg_hours_between_response_and_resolution
FROM customer_tickets
WHERE first_response_time IS NOT NULL
  AND time_to_resolution IS NOT NULL
  AND julianday(time_to_resolution) >= julianday(first_response_time)
GROUP BY ticket_priority
ORDER BY avg_hours_between_response_and_resolution DESC;


-- QUERY 5
-- Compare ticket closure rates across different support channels.
SELECT
c14,
COUNT(*) AS total_tickets,
SUM(CASE WHEN c18 = 'True' THEN 1 ELSE 0 END) AS closed_tickets,
ROUND(
100.0 * SUM(CASE WHEN c18 = 'True' THEN 1 ELSE 0 END) / COUNT(*),
2
) AS closure_rate
FROM customer_tickets
GROUP BY c14
ORDER BY closure_rate DESC;