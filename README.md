<<<<<<< HEAD
Flask on OpenShift
==================

This git repository helps you get up and running quickly w/ a Flask installation
on OpenShift.


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a python-2.6 application

    rhc app create -a flask -t python-2.6

Add this upstream flask repo

    cd flask
    git remote add upstream -m master https://github.com/openshift/flask-example.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://flask-$yournamespace.rhcloud.com

=======
yt2db
=====

Download YouTube video to you Dropbox
>>>>>>> 74d920b4071783d5b7f230fc57c688af9212a689
