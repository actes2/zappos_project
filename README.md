

# Zappos Take Home Challenge
This repo *exists entirely* for the purpose of the Zappos Take Home interview Challenge 

_____

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
    - Custom CSS stylizations in-line and sourced
    - Duck Image Generator hidden in non-session "/admin" attempts.

* Universally Deployable to any database (requires an 'accounts' table with 3 columns for 'key', 'username', 'password' on an SQL server)

# Options for deployment
  - Docker
    > Leverage the python script included for "Deploy_Docker_container.py"
  - AWS CDK for ECS deployment
    > Leverage the python script included for: "Deploy_ECS.py"
  - Standard deployment
    > On any device leverage the "start_Server.py" to automatically host the server off port: 80 on your current device.
# To-do (Hopefully this will all be struck out upon completion)

  * Create our structure "off the bat" for a good layout.
      - Assemble:
        * deploy_ECS.py
        * deploy_Docker.py
        * start_Server.py
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

  - ~~Get SAML up and running. (Maybe we'll keep the simple login for easy Admin Access in this context)~~ * no saml or oauth due to lack of a familiar identity provider in this scenario ( If I had a private enterprise grade azure tenant or AWS instance that'd be a different story ) *
    
  * Dockerize/containerize our application!
      - Make an ubuntu container that 'hands off' installs everything we need to run our application (including deps)!
      - To make it more convenient pipe and source our configuration from this public repo!
      - Include a start-up BASH script that assembles our server configurations, creates our locations for things and executes on-run-time with PORT params with the default value being 80 (Most relevant)
      - Passthrough PORT through localhost:PORT in our configuration so that even on localized systems this container leverages the hosts network
  * Deployment script for docker
    
  * AWS CDK deployment script
      - Begin construction on the AWS CDK deployment script post Docker Container assembly due to this part being marginally easier with the precursor reference.
      - Have our script automatically deploy a ECS container/instance
  
