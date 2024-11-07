# Loco Home Residential Backend

A Django backend application designed to support residential communities in managing complaints, facility bookings, payments, visitor check-ins, and emergency services access. This backend is deployed on Render, supporting the Loco Home Residential App with advanced integrations for complaint analysis and enhanced management processes.

This project initially started as a university course project using Flutter and Firebase but was later improved with Django for a more robust and scalable solution. Currently, this is a prototype without authentication, serving as a proof of concept for an improved residential management system.

Frontend Repository: [Loco Residence Frontend](https://github.com/evelynnn03/loco_residence_frontend.git)

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
  - [Important Note](#important-note)
- [Generating Dummy Data](#generating-dummy-data)
- [Django Apps](#django-apps)
- [Contributors](#contributors)

## Overview

The Loco Home Residential Backend provides a centralized platform for managing various aspects of residential community life, such as complaint handling, facility booking, secure payment processing, and visitor management. Designed to integrate seamlessly with the Loco Home Residential App, the backend enables advanced AI-driven complaint analysis and similarity checks to optimize community interactions and resources.

## Key Features

### Complaint System with Gemini API Integration
- **Clarity, Sensitivity, and Accuracy Checks**: The Gemini API analyzes the topic, description, and images of complaints to prioritize sensitive or urgent issues
- **Similarity Check**: When residents submit a complaint, they can view similar past complaints and their statuses to reduce duplicates
- **Efficient and Holistic**: This system improves management's ability to allocate resources by identifying recurring issues

### Additional Features
- **Facility Booking**: Book community facilities based on real-time availability
- **Payment Processing**: Secure system for resident payments with saved card functionality
- **Visitor Management**: QR code-based check-in/check-out system
- **Emergency Contact Access**: Quick access to emergency and essential service contacts

## Getting Started

### Prerequisites
- Python 3.x
- Django
- An IDE (e.g., PyCharm or Visual Studio Code)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/evelynnn03/loco_residence_backend.git
cd loco_residence_backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Server

1. Apply migrations:
```bash
python manage.py migrate
```

2. Start the development server:
```bash
python manage.py runserver
```

### Important Note
If running locally, you need to:
1. Obtain your own Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project root
3. Add your API key to the `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```

## Generating Dummy Data

To populate the application with sample data:
```bash
python manage.py generate_all_dummy_data <number of residents>
```

## Django Apps

The project consists of the following main apps:
- **Announcements**: Community announcement management
- **Bookings**: Facility reservation system
- **Complaints**: Resident complaint processing with Gemini API integration
- **Finances**: Payment and transaction management
- **Parking**: Resident and visitor parking management
- **Residence**: Resident profile and housing information
- **Visitors**: Visitor check-in/check-out system

## Contributors
- [doodledaron](https://github.com/doodledaron)
- [evelynnn03](https://github.com/evelynnn03)
