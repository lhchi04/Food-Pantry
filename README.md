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
1. **Main Page**: Acts as the central hub, talks to **User Service**, **Catalogue Service**, and **Recipe Service**
1. **User Service**: Manages user registration, login, and profile management, talks to **Recipe Service**
2. **Catalogue Service**: Displays available ingredients for users to select from, talks to **User Service** and **Recipe Service**.
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
- Python Flask
- Flask-RESTful
- spoonacular API (for recipe generation)
- Kubernetes
- Docker

## Features (Minimum Viable Product)
- User registration and authentication
- Browse available ingredients
- Select ingredients
- Generate recipes based on selected ingredients

## Citations
- Spoonacular API: https://spoonacular.com/food-api