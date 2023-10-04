

# Zappos Take Home Challenge
This repo *exists entirely* for the purpose of the Zappos Take Home interview Challenge 

_____
# Post Production Notes
This project was an absolute blast as a whole, I got to utilize and leverage many different skills, experiences, and knowledge in a way that I don't really get a good excuse to do. So for busy work, it 100% scratched my creative itch.

I definitely plan on leveraging a "version" of this for my own lab as it's quite a neat little tool.

Aside from that, I am proud of how the whole thing came together towards the end and believe that this is a good reflection of my skill-sets.


# **Application Overview**
* Backend:
    - *Flask* web framework
    - Hand baked API for crosstalk between front and backend
    - Multiple layers of security and encryption for session privatization and credential storage
    - Language: Python
    - ~~DynamoDB cloud~~ SQL/MySQL based
    
* Front-end:
    - Bootstrap CSS
    - Javascript
    - Custom CSS stylization's in-line and sourced
    - Duck Image Generator hidden in non-session "/admin" attempts. See: 
    - pagination for each table: 10, 25, 50, 100 per page.
    - Searchable and Filterable Datatable
    - Unique gradients per page *It's cool to me*
    - Dynamic CSS/HTML element population on a per-page basis (If you open a table with 19 columns vs 3, the panel will automatically add those columns to your modification options)
    - Reactive table for modifying data via onclick


* Full support for performing CRUD based operations on any DB on the fly with a slick menu that supports swapping between all tables the account defined in .env has access to! *

* Universally Deployable to any database (requires an 'accounts' table with 3 columns for 'key', 'username', 'password' on an SQL server)

# Access a Live Cloud Demo on the web! (Hosted via an AWS EC2 Instance)

**As of 10/3/2023**

I've gone ahead and hosted the application in its own EC2 instance on the cloud:
Feel free to access it via: 

### http://actesco.org/zappos/

The database being leveraged in this instance is hosted on itself

# Standard deployment and Requirements (Manual Only)

To utilize main.py, you will need to include a .env file in the root directory of the application.

This .env file should contain the following environment variables:

```
SQL_USERNAME="SQL Username here*"
SQL_PASS="SQL Password here"
HOST="Hostname here"
DATABASE="Database name on above host here"
SESSION_KEY="Anything here"
```

Then run "main.py" to automatically host the server off port: 80 on your current device.
     
> Additionally, if you would like to use "populate_db.py" or create accounts: See `setup.sql` for database schema

# Options for deployment
  - Docker
    > `docker build -t zappos .`
    
    > `docker run --name zappos-container -p 8080:80 -d zappos`
    
    > Open any web-browser and navigate to 127.0.0.1:8080 to view the application. 
  
    > If the container doesn't clean itself up on closing, leverage `docker stop zappos-container`, followed by a `docker rm zappos`

  - Standard deployment

  
    > Be sure to `pip install -r requirements.txt` to properly obtain all the required dependencies!
# To-do (Hopefully this will all be struck out upon completion)

  * Create our structure "off the bat" for a good layout.
      - Assemble:
        * ~~main.py~~
        * ~~start/build docker scripts~~
        * ~~sql_queries.py~~
        * ~~populate_db.py~~
        * ~~encrypt_decrypt.py~~
        *   ~~-> static~~
        *   ~~-> static -> styles.css~~
        *   ~~-> static -> scripts.js~~
        *   ~~-> templates~~
        *   ~~-> templates -> index.html~~
        *   ~~-> templates -> login.html~~
        *   ~~-> templates -> admin.html~~
        *   ~~-> templates -> register.html~~
        *   ~~-> templates -> navbar.html~~
  
  * Fulfill the basic requirements:
      - ~~Make a webpage - leverage bootstrap for the stylization~~
      - ~~Pull elements from our MySql table into an element~~
      - ~~User Authentication (Simple) login/logout~~ *note: definitely accidentally went full down the security rabbit hole and added a few methods for secure encryption for both sessions, user passwords, and literally any database column that reads "password". so that's cool.* 
      - ~~Write down all dependencies for future reference (containerization)~~

> *probably ~~a~~ coffee break somewhere in here!* -> many coffees later

  - ~~Get SAML up and running. (Maybe we'll keep the simple login for easy Admin Access in this context)~~ * no saml or oauth due to lack of a familiar third-party identity provider in this scenario ( If I had a private enterprise grade azure tenant or AWS instance that'd be a different story ) *
    
  * ~~Dockerize/containerize our application!~~
      - ~~Make an ubuntu container that 'hands off' installs everything we need to run our application (including deps)!~~
      - ~~To make it more convenient pipe and source our configuration from this public repo!~~
      - ~~Include a start-up BASH script that assembles our server configurations, creates our locations for things and executes on-run-time with PORT params with the default value being 80 (Most relevant)~~
      - ~~Passthrough PORT through localhost:PORT in our configuration so that even on localized systems this container leverages the hosts network~~
  * ~~Deployment script for docker~~
    
  * ~~AWS CDK deployment script~~ -> Due to time constraints this part of the project had to be cut; that said I did still deploy the application to its own EC2 instance which is similar without auto-deployment.
      - ~~Begin construction on the AWS CDK deployment script post Docker Container assembly due to this part being marginally easier with the precursor reference.~~
      - ~~Have our script automatically deploy a ECS container/instance~~
  
