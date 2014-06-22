# Merge VIVO URIs

Given pairs of URIs in VIVO, merge assertions from one to the other. This has the effect
of creating a single uri that has all the assertions of both.

## Note

NOTE: Use of merge_uris should be considered extremely dangerous.  merge_uris will
merge *any* two uris.  merge_uris is provided as a means for quickly merging
large numbers of URIs and their related assertions.  It does just that.
It should be used as part of a comprehensive data management activity
to identify and correct data integrity problems in a VIVO triple store.

## What is a merge?

Suppose you have a URI "from" and a uri "to".  merge_uris will remove all statements from VIVO
that match

    from predicate object
	
and all statements that match

    subject predicate from
	
where subject is *any* subject, predicate is *any* predicate and object is *any* object.

Each of these statements is also added to VIVO in the form

    to predicate object
	
and

    subject predicate to
	
All statements about "from" are effectively replaced with the same statements regarding "to".

## How to use merge_uris responsibly

Despite the danger, merge_uris is very handy and can be used responsibly.  Here's a process
that you can use to merge uris without *too much* danger:

1.  Use a query to generate a list of the URIs you want to merge.  Using a query is a good idea --
you can test the query, look at its results and understand why and what uris are going to be merged.
1. Put the query results in a file for use by merge_uris.  The file must have a column called "from" and a 
column called "to".  It can contain any number of additional columns which are ignored by merge_uris.  But you may 
find additional columns useful for providing additional information about the entities being merged -- labels, and
other identifiers are often very useful for the data manager executing the merge.
1. Run merge_uris
1. Inspect the results
    1. Inspect the log results.  In the log, merge_uris shows each URI to be removed.  
	1. Check these results by inspecting
       the objects on the the list in VIVO. to insure that the pairs are as expected.  The "from" will
       be removed and its assertions will be attributed to "to."	   
	1. Check these results by using the [VIVO Triple Inspector](https://github.com/mconlon17/vivo-triple-inspector.git) to see the
       actual statements for each URI.  The Triple Inspector only shows the triples of the form x predicate object.
	   It does not show statements where the specified URI is used as an object.
	1. Inspect the RDF that will be added and subtracted from VIVO.  All the statements should be ones that you 
	   expect regarding a merge of "from" to "to".
1. If you are uncertain about what statements will result from the merge, *STOP!*
1.  If you are *sure* these are the statements you want to remove, then go to the admin menu, select add/remove RDF,
add the add.rdf and remove the sub.rdf.
1.  Save the and add.rdf and sub.rdf files in a safe place in case you made a mistake and need to restore.
1.  Inspect the results in VIVO.  The "from" uris should be gone and the merged "to" entities should look as they
did, but with the addition of information from the corresponding "from" uri.
1. If you made a horrendous mistake, you can remove the add.rdf and add the sub.rdf to restore VIVO, reversing the remove process.
	
Following the steps above, you should be able to use merge_uris and stay safe.

## Some uses for merge_uris

Why do we need such a tool?  Here are some examples of uses:

1.  Combine two profiles that represent the same person.
1.  Combine two departments that represent the same department.
1.  Combine two universities that represent the same university.

## A final note

merge_uris may *create* data integrity problems. Some functional properties (properties that are expected to have one
value) may obtain multiple values -- the value from the "from" and the the value from the "to."  merge_uris knows
several functional properties and does not not allow duplication of the ones it knows.  rdfs:label is considered
single valued by merge_uris.  If "from" and "to" both have labels, only the label from "to" will be present in
the resulting merge.  This behavior may result in loss of information.

## Example 1 -- Merge organizations

See merge_nih.txt.  UF VIVO had many instances of each of the various institutes and centers of the NIH.  The 
file merge_nih.txt is input to merge_uris for the purpose of creating single instances of each of the institutes
and centers.  Not that several "from" uri are merged to single "to" uris -- one for each center and institute.  In this
way all the duplicates are combined.

## Example 2 -- Merge countries

See merge_countries.rq, a SPARQL query for identifying URI that indicate duplicate countires -- that is, the same country
appears in VIVO under two different URI.  The result set, merge_countries.txt, serves as input to merge_uris to merge
all the duplicates to single URI for each country.



