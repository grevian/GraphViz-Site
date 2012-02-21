<!doctype html>  
<cfparam name="url.method" default="dot" />
<cfparam name="url.x" default="5" type="numeric" />
<cfparam name="url.y" default="5" type="numeric" />
<cfparam name="url.result" type="string" default="" />
<cfparam name="url.error" type="string" default="" />
<cfparam name="input" type="string" default="" />
<cfparam name="error" type="string" default="" />

<cfif url.result neq "" or url.error neq "">
	<cfif url.result neq "">
		<cfset file = "#getdirectoryFromPath(getcurrentTemplatePath())#/tmp/#GetFilefrompath(url.result)#" />
		<cfif not fileExists(file) >
		 <cflocation statuscode="404" url="/404.html" />
	    <cfelse>
		 <cffile action="read" file="#file#" variable="input" />
	    </cfif>
	<cfelse>
		<cfset file = "#getdirectoryFromPath(getcurrentTemplatePath())#/tmp/#GetFilefrompath(url.error)#" />
		<cfif not fileExists(file) >
		 <cflocation statuscode="404" url="/404.html" />
	    <cfelse>
	     <cffile action="read" file="#file#" variable="input" />
		 <cffile action="read" file="#file#.error" variable="error" />
	    </cfif>
	</cfif>
</cfif>


<!-- paulirish.com/2008/conditional-stylesheets-vs-css-hacks-answer-neither/ --> 
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
  <meta charset="utf-8">

  <!-- Always force latest IE rendering engine (even in intranet) & Chrome Frame 
       Remove this if you use the .htaccess -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

  <title>MATH2056 Graph Generator - Make a Graph</title>
  <meta name="description" content="">
  <meta name="author" content="">

  <!--  Mobile viewport optimized: j.mp/bplateviewport -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Place favicon.ico & apple-touch-icon.png in the root of your domain and delete these references -->
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">


  <!-- CSS : implied media="all" -->
  <link rel="stylesheet" href="css/style.css?v=2">

  <!-- Uncomment if you are specifically targeting less enabled mobile browsers
  <link rel="stylesheet" media="handheld" href="css/handheld.css?v=2">  -->
 
  <!-- All JavaScript at the bottom, except for Modernizr which enables HTML5 elements & feature detects -->
  <script src="js/libs/modernizr-1.6.min.js"></script>

</head>

<body>

  <div id="container">
    <header>
		<h1>Unofficial MATH2056 Graph Generator</h1>
		<nav>
		 <ul>
		 <li><a href="index.html">Home</a></li>
		 <li><a href="documentation.html">Documentation</a></li>
		 <li><a href="graph.cfm" class="current">Make a Graph</a></li>
		 <li><a href="about.html">About this Site</a></li>
		 <li><a href="links.html">Related Links</a></li>
		 <li><a href="contact.html">Contact Me</a></li>
		 </ul>
		</nav>
    </header>
    
    <div id="main">
    <h2>Make A Graph</h2>
	<p>Enter your <code class="inline">DOT</code> definition in the box below, and click Generate to display the resulting graph.</p>
	<form method="POST" action="generateGraph.cfm" id="dot-submission">
	 <textarea spellcheck="false" wrap="off" id="dot-input" name="input"><cfif len(input)><cfoutput>#input#</cfoutput></cfif></textarea>
	 <br />
	 <label for="method">Layout Method</label>
	 <select id="method" name="method">
	  <option value="dot" <cfif url.method eq "dot">selected</cfif> >dot</option>
	  <option value="neato" <cfif url.method eq "neato">selected</cfif>>neato</option>
	  <option value="twopi" <cfif url.method eq "twopi">selected</cfif>>twopi</option>
	  <option value="circo" <cfif url.method eq "circo">selected</cfif>>circo</option>
	  <option value="fdp" <cfif url.method eq "fdp">selected</cfif>>fdp</option>
	  <option value="sfdp" <cfif url.method eq "sfdp">selected</cfif>>sfdp</option>
	 </select> (Just use trial and error to find the method you think works best)
	 <br />
  	 <cfoutput>
	  <label for="height">Max Height:</label><input type="text" id="height" name="y" value="#url.y#" size="3" />
	  <label for="width">Max Width:</label><input type="text" id="width" name="x" value="#url.x#" size="3" />
	 </cfoutput>
	 (In Inches of all things)
	 <br />
	 <input type="submit" value="Generate" />
	</form>
	<h2>Results</h2>
	<div id="results">	
	<cfoutput>
	 <cfif url.result neq "" and not len(error) >	
	  <img src="/tmp/#GetFileFromPath(file)#.png" />
     <cfelseif len(error)>
      <p class="error">
	   <h3>Error:</h3>
        #error#
	  </p>
     </cfif>
	</cfoutput>
    </div>
    <footer>
	
    </footer>
  </div> <!--! end of #container -->


  <!-- Javascript at the bottom for fast page loading -->

  <!-- Grab Google CDN's jQuery. fall back to local if necessary -->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.js"></script>
  <script>!window.jQuery && document.write(unescape('%3Cscript src="js/libs/jquery-1.4.2.js"%3E%3C/script%3E'))</script>
  
  
  <!-- scripts concatenated and minified via ant build script-->
  <script src="js/plugins.js"></script>
  <script src="js/script.js"></script>
  <!-- end concatenated and minified scripts-->
  
  
  <!--[if lt IE 7 ]>
    <script src="js/libs/dd_belatedpng.js"></script>
    <script> DD_belatedPNG.fix('img, .png_bg'); //fix any <img> or .png_bg background-images </script>
  <![endif]-->

  <!-- asynchronous google analytics: mathiasbynens.be/notes/async-analytics-snippet 
       change the UA-XXXXX-X to be your site's ID -->
  <script>
   var _gaq = [['_setAccount', 'UA-10594743-3'], ['_trackPageview']];
   (function(d, t) {
    var g = d.createElement(t),
        s = d.getElementsByTagName(t)[0];
    g.async = true;
    g.src = ('https:' == location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    s.parentNode.insertBefore(g, s);
   })(document, 'script');
  </script>
</body>
</html>
