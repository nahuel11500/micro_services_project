## Project Overview

This project is part of a school course led by Professor Helene Coullon, and you can find more about her work at [helene-coullon.fr](https://helene-coullon.fr/). The initial repository for this project can be found on [GitHub](https://github.com/IMTA-FIL/UE-AD-A1-REST).

The main objective of this project is to gain a comprehensive understanding of micro-service architecture, focusing on the usage of REST APIs, OpenAPI specifications, and the Flask framework.

### Project Tasks

In this project, we tackled the following key tasks:

1. **Movie Service Enhancements**
    - Added custom entry points and updated OpenAPI specifications.

2. **Microservice Testing**
    - Thoroughly tested all microservices with Postman.

3. **Times Microservice Development**
    - Created the Times microservice based on provided OpenAPI specs and rigorously tested it.

4. **Booking Service Implementation**
    - Developed the Booking service according to OpenAPI specifications and conducted comprehensive testing.

5. **User Service Integration**
    - Defined User service OpenAPI specs to interact seamlessly with Booking and Movie services, including reservation retrieval and movie information.

6. **User Service Testing**
    - Developed and tested the User service with Postman.

## Getting Started with Docker Compose

To run this project using Docker Compose for easy deployment and testing, follow these steps:

### Prerequisites

Before starting, ensure you have Docker and Docker Compose installed on your system. You can download and install Docker from [Docker's official website](https://www.docker.com/get-started).

### Running the Project with Docker Composer

1. Clone the project repository
2.Build and start the project with Docker Compose:
`docker-compose up -d`

### Test the Project in Docker Compose

To test the project, you can, in a powershell, run the following command : 
`.\test_oral.ps1 `
It will start the project in containers and run the test.py in user service, that will send some request and print the result. 

### Running the project without Docker

You can also open the project in an Editor and manually start all the services. 
