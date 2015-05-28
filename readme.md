A small time tracking and task management application designed for individuals. This 
project was originally built for my own personal use. Feel free to make suggestions or 
report issues.


FEATURES
========

- Per-project todo lists
- Graphical timetracker interface baked in, integrates with todos
- Generates itemised pdf invoices from billable time on project


INSTALLATION & SETUP
====================

1. Download the latest release and run

        python setup.py install
    
2. Add '`projectmanager`' to `INSTALLED_APPS`, migrate your database, and include 
   `'projectmanager.urls'` somewhere in your urlconf.


FUTURE
======

- Enable more than one user