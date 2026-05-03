# REST API Reliability and Availability Analysis

## Overview
This project analyzes the reliability of a REST API service by repeatedly sending requests to an endpoint and collecting HTTP response codes. The goal was to evaluate how often the service returned successful responses compared to error responses.

## Project Scope
The project included:
- Sending automated requests to a REST endpoint
- Capturing HTTP response codes
- Saving timestamped results in CSV format
- Analyzing response-code frequency and percentage distribution
- Creating visualizations using the collected data
- Calculating service availability
- Preparing a technical report
- Recording a video presentation explaining the implementation and results

## Method
A Bash script was used to send 120 requests at approximately one-second intervals. Each response was stored in a CSV file using the following format:

YYYY-MM-DD HH:MM:SS, HTTP-CODE

## Results

| HTTP Code | Count | Percentage |
|---|---:|---:|
| 200 | 50 | 41.67% |
| 301 | 13 | 10.83% |
| 400 | 18 | 15.00% |
| 403 | 11 | 9.17% |
| 404 | 7 | 5.83% |
| 500 | 21 | 17.50% |

## Availability Calculation
Availability was calculated as:

Availability = Successful Responses / Total Requests

Availability = 50 / 120 = 41.67%

## Conclusion
The service returned successful HTTP 200 responses less than half of the time. This indicates that the service was unreliable during the monitoring period.

## Tools Used
- Bash
- curl
- CSV
- Microsoft Excel
- GitHub
- Video presentation

## Report
[View Report](report.pdf)

## Video Demonstration
[Watch Video](https://www.youtube.com/watch?v=39QnVrCDIPc)
