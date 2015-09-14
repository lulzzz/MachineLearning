select * 
	from crosstab (
		$$select 
			docid varchar, 
			yyyy float8, 
			rowtype varchar, 
			txtmark varchar
		from ted.tmp_security
		where rowtype = ANY ('{title, description}')
		group by docid, yyyy, rowtype, txtmark
		order by 1,2$$
	)
AS 
	ct (docid, 
	yyyy,
	"title", 
	"description"
	);