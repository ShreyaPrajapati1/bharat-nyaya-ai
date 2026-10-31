# Bharat Nyaya AI — Team 4 Testing Report

## Website Testing

| Test ID | Test Case | Result |
|---|---|---|
| TC-01 | FIR-001 View | PASS |
| TC-02 | FIR-002 View | PASS |
| TC-03 | FIR-003 View | PASS |
| TC-04 | Status Dropdown | PASS |
| TC-05 | Go to FIR Tracking | PASS |
| TC-06 | Empty FIR Number | PASS |
| TC-07 | Invalid FIR Number | PASS |
| TC-08 | FIR Status Tracking | PASS |
| TC-09 | Admin–Tracking Status Sync | PASS |
| TC-10 | Tracking Status After Refresh | PASS |

**Observation:** FIR status Admin Dashboard se update karne ke baad Tracking page par bhi dikh raha hai. Refresh ke baad FIR number dobara enter karna padta hai.

**Fix Implemented:** FIR-001 status ko browser ke localStorage mein save aur retrieve kiya ja raha hai.

## Postman API Testing

| Test ID | Test Case | Result |
|---|---|---|
| API-01 | GET request to Postman Echo API | PASS |

**Request Method:** GET

**API URL:** https://postman-echo.com/get

**Expected Result:** API should return a successful response.

**Actual Result:** Received 200 OK with JSON response.

**Response Time:** 1.84 seconds

**Status:** PASS

**Note:** Postman Echo API is a demo API. This test does not test the Bharat Nyay AI backend.
