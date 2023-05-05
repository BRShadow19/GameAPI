<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h2 align="center">GameAPI</h2>

  <p align="center">
    A unified API wrapper for game services
    <br />
    <a href="https://github.com/brshadow19/GameAPI/issues">Report Bug</a>
    ·
    <a href="https://github.com/brshadow19/GameAPI/issues">Request Feature</a>
  </p>
</div>
<br />

[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield-brenden]][linkedin-url-brenden]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#api-tokens">API Tokens</a></li>
        <li><a href="#running-as-a-python-application">Python Application</a></li>
        <li><a href="#docker">Docker</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project started as a final for my CS-475 Computer Networks course at Ursinus, and developed into something that is now in daily use with my friends and I. We built a [Discord bot](https://github.com/BRShadow19/discord-bot) and were wanting to add some game integrations into it, but never had the time to really dig into the various APIs of the games that we play. So, I decided that my CS-475 final project would give me the time I needed to learn more about using and building APIs.

This program consists of a [Flask](https://flask.palletsprojects.com/en/2.3.x/) server that can be called through HTTP requests, and separate files for code that interfaces with the API of each game. Right now, the program can get stats on League of Legends using the [Riot API](https://developer.riotgames.com/docs/lol), but I plan to add more games in the future. 

This program is coded completely in Python and can be run as a Python script, or in a Docker container with the provided [Dockerfile](https://github.com/BRShadow19/GameAPI/blob/main/Dockerfile). I currently run both this and our [Discord bot](https://github.com/BRShadow19/discord-bot) in two Docker containers, using Docker's [container networking](https://docs.docker.com/config/containers/container-networking/) to allow communication between the two programs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

This program can be run either as a set of Python scripts, or in a Docker container. Regardless of your choice, there are some API tokens that you will need in order for the program to work. To start, clone this repository into a local directory on your machine.


### API Tokens
First, make a file called `token.env` within the main directory of the program code. Now we will start to fill it with our API tokens. If you choose to use Docker, instead enter the API keys in the corresponding spots in `Dockerfile` (for the Dockerfile you should **not put the key values within quotes**, unlike how it is shown below).
* Riot API Token
  * Head over to Riot's [Developer Site](https://developer.riotgames.com/) and create an account, or log in with an existing Riot Games account. You can either use the Development API Key (only lasts 24 hours), or [submit an application](https://developer.riotgames.com/docs/portal#product-registration_application-process) for a product that will get you a permanent API key.
    * I use a Personal API Key, which has the same rate limits as the Development key, but does not have to be manually regenerated every 24 hours.
  * Grab your API token and add it to your `token.env` file like so:
  ```sh
  # Riot API Key
  RIOT_KEY='*********************'
  ```

This will be updated with more API key instructions as we add support for more games

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Running as a Python application

Below is a list of Python modules that you will need to install in order for the bot to work properly. We recommend creating a Python [virtual environment](https://docs.python.org/3/library/venv.html) to ensure that you always have the correct version for this specific program.
* [Flask](https://flask.palletsprojects.com/en/2.3.x/installation/) - HTTP Server for interfacing with the program
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Read in environment variables from `token.env`
* [requests](https://pypi.org/project/requests/) - Python  HTTP Library

All of these can be installed using the included [requirements.txt](https://github.com/BRShadow19/GameAPI/blob/main/requirements.txt) with the below command from within this program's directory:
```sh
  pip install -r requirements.txt
  ```
Now, you should have everything you need for the program to work. Simply run `game_api.py` to start it up!
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Docker
This guide will assume you already have Docker installed and working on your machine. If not, follow [this documentation](https://docs.docker.com/get-started/) to get started with Docker.
* Build the image
  ```sh
  # From inside the root of the program directory
  docker build -t containername
  ```
* Run the application
  ```sh
  docker run -d -it -p 5000:5000 --network host --name=CONTAINER_NAME
  ```
And that's it! The program should be up and running now. You can use
```sh
docker attach CONTAINER_NAME
```
to attach the container to your terminal and check for any errors. If you have the default keybinds for docker, you can detatch the container by using CTRL+P then CRTL+Q.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.
<br />
<br />
<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->


<!-- CONTACT -->
## Contact

Brenden Reim - brenden@breim.dev

Project Link: [https://github.com/brshadow19/GameAPI](https://github.com/brshadow19/GameAPI)

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->
<br />
<br />

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments


* [Riot API](https://developer.riotgames.com/)
* [Flask](https://flask.palletsprojects.com/en/2.3.x/)
* [Docker](https://docs.docker.com/)
* [Ursinus CS-475](https://www.billmongan.com/Ursinus-CS475-Spring2023/)
* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BRShadow19/GameAPI?color=gr&style=for-the-badge
[contributors-url]: https://github.com/BRShadow19/GameAPI/graphs/contributors
<!-- [forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge -->
<!--[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members -->
[stars-shield]: https://img.shields.io/github/stars/BRShadow19/GameAPI?style=for-the-badge
[stars-url]: https://github.com/BRShadow19/GameAPI/stargazers
[issues-shield]: https://img.shields.io/github/issues/BRShadow19/discord-bot?style=for-the-badge
[issues-url]: https://github.com/BRShadow19/discord-bot/issues
[license-shield]: https://img.shields.io/github/license/BRShadow19/GameAPI?style=for-the-badge
[license-url]: https://github.com/BRShadow19/GameAPI/blob/main/LICENSE
[linkedin-shield-brenden]: https://img.shields.io/badge/LINKEDIN-Brenden-blue?style=for-the-badge
[linkedin-url-brenden]: https://linkedin.com/in/brenden-reim