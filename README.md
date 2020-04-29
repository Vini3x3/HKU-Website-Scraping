# Pythonic and Structural Upgrade

In order to make things more pythonic, this version adopts PEP-8 standards.   

To make things better and more maintainable, there are 2 points to be upgraded in this version: 

- `webmaster.py` : extend from`thread.timer` instead of containing a thread
- `HKUSites.py`: use decorator for probing and caching

