# Data Model Specification

## Overview

This document defines the canonical event model used by the pipeline.

Important identifier rule: `customer_id` is the canonical identifier because the downstream mbilling system keys on customer, not user.

## Event Types

The pipeline treats `event_type` as a normalized string (lowercased and trimmed). Known event types in current usage are:

- `click`: A user/customer interaction representing a click action.
- `page_view`: A user/customer interaction representing a page view action.
- Other normalized values: Additional event types are allowed as long as they are provided as strings and normalize to lowercase/trimmed text.

## Canonical Event Schema

Each event record should contain the following fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `customer_id` | string | Yes | Canonical customer identifier for attribution, aggregation, and downstream joins. |
| `event_type` | string | Yes | Event category, normalized to lowercase and trimmed (for example, `CLICK` -> `click`). |
| `timestamp` | string | Yes | Event time in string form (expected ISO-8601 UTC format, for example `2026-01-01T00:00:00Z`). |
| `value` | number | No (defaults to `0.0`) | Numeric payload associated with the event, used in rollups and totals. |
| `metadata` | object | No (defaults to `{}` during normalization/enrichment) | Optional extensible key-value attributes derived or attached during processing. |

## Raw Input to Canonical Mapping

When ingesting raw records, these source keys map to canonical fields:

- `customer_id` -> `customer_id`
- `type` -> `event_type`
- `ts` -> `timestamp`
- `value` -> `value`

## Consumers That Depend on the `customer_id` Field Name

The following consumers rely on the identifier field being named `customer_id` in the published event contract:

- Downstream mbilling ingestion and keying logic (customer-level billing joins).
- JSONL export consumers that parse event identifiers from serialized records.
- Reporting and aggregation consumers that group and sum events by customer identifier.
- Automated tests/contract checks that validate identifier field naming in pipeline outputs.
