# cpsc415-project
# Recipe Store

## Application and purpose
RecipeFinder is a comprehensive web application designed to simplify the process of discovering and generating recipes based on selected ingredients. Our purpose is to offer users a seamless experience in finding and creating delicious meals using our ingredients.

## Members
1. Chi Le
2. Vy Sa Nguyen
3. Shazif Ahmed

## Description
The Online Thrift Store is a web application that allows users to browse and add second-hand items to cart. The application consists of 4 main services:
1. **Main Page**: Serves as the central hub, facilitating communication between other services and managing the overall workflow.
Acts as the central hub, talks to **User Service**, **Catalogue Service**, and **Recipe Service**
1. **User Service**: Handles user registration, login, and profile management.
Manages user registration, login, and profile management, talks to **Recipe Service**
2. **Catalogue Service**: Displays a catalog of available ingredients for users to select from.
Displays available ingredients for users to select from, talks to **User Service** and **Recipe Service**.
3. **Recipe Service**: Generates recipes based on the ingredients chosen by the user.

The architecture of the application is designed with microservices in mind, leveraging Python Flask for building the services. Each service communicates with others via RESTful APIs, and the application is deployed on Kubernetes for scalability and reliability.

## UI
The UI of the Online Thrift Store is built using HTML and CSS, offering an intuitive experience for selecting ingredients and viewing generated recipes.

## Build, Run, Deployment Instructions



## Application Usage Instructions
[Provide instructions for users on how to interact with the application. Include how to register, browse items, add items to the cart, and use the chatbot feature.]

## Component Diagram

![Architecture](./uml-diagram.jpeg)

## Screenshots/GIFs

## Dependencies
- Flask-RESTful: An extension for Flask that adds support for quickly building REST APIs.
- spoonacular API: An API for recipe generation and food data.
- Kubernetes: An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.
- Docker: A platform for developing, shipping, and running applications in containers.

## Features (Minimum Viable Product)
- User registration and authentication
- Browse available ingredients
- Select ingredients
- Generate recipes based on selected ingredients

## Data Transmitted Between Services
### Main Service and User Service
1. **User Authentication**: The Main Service sends user authentication requests to the User Service, including login credentials and registration data.
2. **User Profile Management**: The User Service provides endpoints for managing user profiles, allowing the Main Service to retrieve and update user information.

### Main Service and Catalogue Service
1. **Ingredient Catalog**: The Catalogue Service sends ingredient data to the Main Service, allowing users to browse and select ingredients for recipe generation.

### Main Service and Recipe Service
1. **Recipe Generation Requests**: The Main Service forwards user-selected ingredients and preferences to the Recipe Service to generate personalized recipes.

### Error Handling
Appropriate error messages or status codes are transmitted between the microservices to handle exceptions and provide user feedback.

## Citations
- Spoonacular API: https://spoonacular.com/food-api