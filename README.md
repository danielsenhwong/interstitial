# interstitial
## Introduction
A number of laboratory inventory management systems (LIMS) are available, \
but nearly all are commercial, with user data monetized and used to support \
ongoing development and operation. This presents some opportunities for \
supply companies, but also privacy concerns for research groups.

The current and forseeable research environment is extremely competitive, and \
the use of LIMS provides advantages in operational efficiency that allow \
scientists and staff to focus on their research work instead of maintaining \
shared spreadsheet and paper records.

This project, 'interstitial,' is intended to be an open-source LIMS developed \
in Python using the Django framework. Given the popularity of Python in \
biomedical and data science, this should keep the source code accessible to \
a large part of the scientific community, lowering the barrier to entry and \
ensuring longevity of the project.

## Changes
### 14 Jan 2017
Pushed 'interstitial' project to git. Collected static content, created data\
base. Started development with 'institutions' app/model.

App secret and database configuration files in user home directory, \
~/project_secrets/ in *.txt and *.cnf files.
