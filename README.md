# Sentiment Analysis and Product Review Classification

## Project Overview

This project implements a sentiment analysis and product review classification system using machine learning techniques. The application allows users to submit reviews about a product (specifically shoes) and receive feedback on the sentiment of various aspects such as the sole, toe, and quality of the shoe.

## Features

- **Review Submission**: Users can submit their product reviews through a user-friendly interface.
- **Aspect Extraction**: The application extracts key aspects from the review using keyword matching.
- **Sentiment Analysis**: Reviews are analyzed for sentiment using a pre-trained DistilBERT model to classify the sentiment as positive or negative.
- **Interactive UI**: Users can click on different parts of a shoe image to view sentiment analysis specific to those areas.

## Technologies Used

- **Backend**: 
  - Flask: A Python web framework for building the API.
  - Transformers: For using the pre-trained sentiment analysis model.
  
- **Frontend**:
  - React: For building the user interface.
  - CSS: For styling the application.

## Installation
  - pip install Flask Flask-CORS transformers torch

### Prerequisites

- Python 3.x
- Node.js and npm (for the React frontend)

### Clone the Repository

```bash
git clone <repository-url>
cd sentiment-analysis-product-review
