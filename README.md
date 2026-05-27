# SafeTrack WA — Mine Safety Incident Migration Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-Containerised-blue)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![License](https://img.shields.io/badge/Licence-CC--BY--4.0-green)

## Overview

SafeTrack WA is an end-to-end data migration and analytics platform simulating a real-world enterprise scenario: transforming legacy mine safety records from multiple Western Australian operations into a modern, structured, and scalable system.

The project covers the complete pipeline — from raw data ingestion and ETL processing, through relational schema design and REST API development, to containerised deployment and Power BI analytics.

---

## Problem Statement

Mining operations across Western Australia generate vast volumes of safety data every day — incident reports, near-miss logs, inspection findings, and corrective action records. In many operations, this data remains locked in disconnected spreadsheets and legacy systems that cannot communicate with each other.

This fragmentation creates serious operational and regulatory risk:

- Safety managers cannot calculate TRIFR (Total Recordable Injury Frequency Rate) in real time
- Near-miss data sits in shift supervisor notebooks and never reaches decision makers
- Corrective actions from inspections go untracked, leaving compliance gaps
- Site managers have no cross-site visibility into hazard patterns

SafeTrack WA addresses this by migrating legacy safety data into a normalised PostgreSQL schema, exposing KPIs via a Flask REST API, and delivering real-time insights through a Power BI dashboard.

---

## System Architecture