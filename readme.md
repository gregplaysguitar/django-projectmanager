A small time tracking and task management application designed for individuals. This 
project was originally built for my own personal use. Feel free to make suggestions or 
report issues.


FEATURES
========

- Per-project todo lists
- Graphical timetracker interface baked in, integrates with todos
- Generates itemised pdf invoices from billable time on project
- Builds on django's built-in admin, using admin views where possible.


INSTALLATION & SETUP
====================

1. Download the latest release and run

        python setup.py install
    
2. Add '`projectmanager`' to `INSTALLED_APPS`, migrate your database, and include 
   `'projectmanager.urls'` somewhere in your urlconf.

3. Copy the `projectmanager/templates/admin` folder into your main templates directory,
   so that django can find it. This will include projectmanager links at the top of every
   admin page.

4. For invoice generation, you'll need to create your own 
   `projectmanager/pdf/invoice.html` template, overriding 

5. Add `PROJECTMANAGER_HOURLY_RATE` and `PROJECTMANAGER_SALES_TAX` to your settings to
   customise.

FUTURE
======

- Enable more than one user