# shuffleboard

## A Kodi plugin for my home media center.

### Installation: How I do it (YMMV)
1. ssh into the machine I use to run Kodi
2. (first time only!) clone this repo into `~/.kodi/addons/script.shuffleboard`
3. cd into `~/.kodi/addons/script.shuffleboard`, `git pull` to get whatever updates I've made

That's it. Once I have a stable (read: more than proof-of-concept) setup, I'll probably have a "stable" branch for normal use and a "development" branch for that purpose, but let's not get ahead of ourselves.

### Pre-v1 progress and plans:
* v0.0.1 (done)
  * finds all happy endings episodes
  * shuffles that list, and queues them all

* v0.0.2 (done)
  * add repeat "ON"
  * use config file to define show (still just one for now)
  * clean up repo for easy download-n-installing

* v0.0.3 (done)
    * Cleanup release! Single script is getting large and unwieldy, need to do some refactoring now that things are working before moving on to more advanced features
    * same net effect, but clean up code to use multiple classes, be "clean", ~~add unit tests~~, etc
    * Issues added to github page for future v0.x work items

* v0.0.4 and beyond
    * multiple shows in config, flip between them.
    * able to configure shows used in options menu rather than pre-defined text file

Might consider cutting v1.0 release at this point, we'll see.

### Future considerations:
* specify in-order vs random (done)
* show upcoming schedule somehow (doubt this happens, given the "make a playlist, queue it, then exit" shape development has taken)
* allow for "N episode chunks"
* mix shows if desired
* resume/return to where last watching (should definitely be able to get this working)
* more features? I'll add things as I think of them
