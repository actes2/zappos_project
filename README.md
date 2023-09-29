

# Zappos Take Home Challenge
This repo *exists entirely* for the purpose of the Zappos Take Home interview Challenge 

_____

# **Application Overview**
* Backend:
    - *Flask* web framework
    - Language: Python
    - SAML
    - DynamoDB cloud based replace for mysql database in this context
* Front-end:
    - Bootstrap CSS
    - Javascript
    - AJAX
* SAML Authentication
* Fluid deployment

# Options for rapid deployment
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
        *   ~~-> static~~
        *   ~~-> static -> styles.css~~
        *   ~~-> static -> scripts.js~~
        *   ~~-> templates~~
        *   ~~-> templates -> index.html~~
        *   ~~-> templates -> login.html~~
        *   ~~-> templates -> admin.html~~
        *   ~~-> templates -> register.html~~
  
  * Fulfill the basic requirements:
      - Make a webpage - leverage bootstrap for the stylization
      - Pull elements from our DynamoDB table into an element
      - User Authentication (Simple) login/logout
      - Write down all dependencies for future reference (containerization

> *probably a coffee break somewhere in here!*

  * Get SAML up and running. (Maybe we'll keep the simple login for easy Admin Access in this context)
    
  * Dockerize/containerize our application!
      - Make an ubuntu container that hands off installs everything we need to run our application (including deps)!
      - To make it more convenient pipe and source our configuration from this public repo!
      - Include a start-up BASH script that assembles our server configurations, creates our locations for things and executes on-run-time with PORT params with the default value being 80 (Most relevant)
      - Passthrough PORT through localhost:PORT in our configuration so that even on localized systems this container leverages the hosts network
  * Deployment script for docker
    
  * AWS CDK deployment script
      - Begin construction on the AWS CDK deployment script post Docker Container assembly due to this part being marginally easier with the precursor reference.
      - Have our script automatically deploy a ECS container/instance
  
