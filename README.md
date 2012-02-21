# GraphViz for Discrete Math Students

This project is a simple web interface to GraphViz using Coldfusion to interact
with dot, I wrote it while taking the MATH2056 course at Algoma University, to
help myself and others who needed to draw graphs for various problems including
Euler and Hamiltonian Circuits and Paths, as well as Dijkstra's Algorithm and
other graph and tree applications. I wrote a set of examples and a quick
reference for the features I found myself using, and wrapped it all up in an
HTML-5 Boilerplate template 

## Setup

I hosted this on an OpenBlueDragon on Tomcat platform, setting up your JSP and
CFML platforms is your own business though it's pretty easy to do these days,
Once that's done just place this project in your CFML webapps/ directory, or
serve the app from wherever you like using your JSP server and mod_redirect as
needed. 

## Caveats

* I recommend a cron-job to empty out $site_root/tmp/ every once in a while, the frequency will depend on how heavily used the site is
* It's possible there is an information disclosure vulnerability in this site, related to custom shapes and other DOT language features that reference external files, most sane JSP servers will have a security policy that mitigates this already, and most sane *nix platforms will have system permissions that prevent anything too juicy from being exposed. But I thought I should say it just in case.


