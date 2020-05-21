# Notification

Build on top of the Web Scraping Module, Notification class is a control of webmaster to monitor and arrange notification.    However, the ultimate aim of the notification class is to make it easy and understandable, as the remaining time for development is short.  

At first glance, the notification class should have the following structure: A notification runtime environment with a list of observer class.  The notification runtime is for managing the notification list, just like webmaster; the list of observer class is extendable to its superclass, an observer, and adopting factory pattern.  

To make it even more simpler, the notification runtime only issue command to the webmaster so that we can isolate the webmaster.  