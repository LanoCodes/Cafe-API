# Café API
- This project is an API created using Python's Flask and Flask SQLAlchemy!
- Postman was also used for making requests to the API!

## What's Its Purpose?
- This API helps you interact with a database containing a collection of cafés in the London, UK area. 
- It's an exploration into building an API and its corresponding documentation. The server itself isn't publicly available, but will be made available to you after downloading the project to you machine and running it there.

## Functionality
- This API has 6 endpoints total
  - GET
    - Search Cafés By Location
    - Get All Cafés
    - Get Random Cafes
  - POST
    - Add Cafe
  - PATCH
    - Update Price of Coffee at Café
  - DELETE
    - Delete Café by ID
- You can find the publicly available documentation I created on Postman [here](https://documenter.getpostman.com/view/15465500/2s9Y5VU4et) 


## Installation
- Here, I'll outline how you can get this project onto your machine and begin interacting with the API.
1. Create a directory on your machine to house it, "CafeAPI" could work
   1. On Mac, use terminal for below:
   ```commandline
   mkdir CafeAPI
    ```
2. Look above on this page and select "Code"
3. From here, copy the HTTPS web URL
4. Return to your terminal and clone the repo
   ```commandline
   git clone https://github.com/LanoCodes/Cafe-API.git
    ```
5. I used PyCharm, but using your preferred IDE, open the CafeAPI project
6. There are some prerequisites to actually running the project!:
   1. First you'll need to make sure that the all the requirements have been downloaded
7. After you have the necessary requirements installed you can now run main.py and use a service like Postman to make requests to the running server.
   - Be sure to follow the documentation!
