<cfif not isdefined("form.input") or form.input eq "" >
 <cflocation statuscode="411" url="graph.cfm" />
</cfif>

<cfparam name="form.x" type="numeric" default="5" />
<cfparam name="form.y" type="numeric" default="5" />
<cfparam name="form.method" type="string" default="circo" />

<!--- Generate a temporary file in the local tmp directory, and write our form submission out to it --->
<cfset currentDir = getdirectoryFromPath(getcurrentTemplatePath()) />
<cfset TempFile = GetTempFile("#currentDir#/tmp/", "dot") />
<cffile action="write" file="#TempFile#" output="#form.input#" addnewline="false" />

<!--- Generate the graph, storing the output location and possible error file output location --->
<cfset Output = "#currentDir#/tmp/#getfileFromPath(TempFile)#.png" />
<cfset Error = "#currentDir#/tmp/#getfileFromPath(TempFile)#.error" />
<cfset quickResults = ""/>

<cfif ListContainsNoCase("dot,neato,twopi,circo,fdp,sfdp",form.method) gt 0 >
 <cfexecute name="/usr/bin/dot" arguments="#TempFile# -Tpng -Gsize=#x#,#y# -Glayout=#form.method# -o#Output#" errorFile="#Error#" timeout="5" />
 <cfelse>
 <cfabort />
</cfif>
 
<!--- If the output generated successfully, show it, otherwise show the error --->
<cfoutput>
 <cfif FileExists("#Output#") >
  <cflocation statuscode="200" url="http://#cgi.server_name#/graph.cfm?result=#getfileFromPath(TempFile)#&x=#form.x#&y=#form.y#&method=#form.method#" />
 <cfelse>
  <cflocation statuscode="500" url="http://#cgi.server_name#/graph.cfm?error=#getfileFromPath(TempFile)#" />
</cfif>
</cfoutput>
