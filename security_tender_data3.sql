drop table ted.tmp_security;

create table ted.tmp_security as
select D.id as docid, extract(YEAR FROM D.datepub) as yyyy, E.timark, E.txtmark
from ted.tender_cpv A
inner join ted.tender B on A.tender_id = B.id
inner join ted.ref_cpv C on A.cpv_code = C.code
inner join ted.tender_document D on B.id = D.tender_id
inner join ted.en_document_text E on D.id = E.doc_id
inner join ted.ref_nat_notice N on D.natnotice = N.code
where 
	B.isocountry = 'UK' and 
	upper(N.en) = 'CONTRACT NOTICE' and
	(upper(E.timark) like 'SHORT DESCRIPTION%' or
	upper(E.timark) = 'DESCRIPTION' or
	upper(E.timark) like 'TITLE') AND
	
	(A.cpv_code like '7971%' or
	A.cpv_code like '3512%' or
	A.cpv_code like '452223%' or
	A.cpv_code like '4873%' or
	A.cpv_code like '5061%' or
	A.cpv_code like '7221273%' or
	A.cpv_code like '734%' or
	A.cpv_code like '73421%' or
	A.cpv_code like '73431%' or
	A.cpv_code like '75241%' or
	A.cpv_code like '79721%' or
	A.cpv_code like '8060%')
	
group by docid, yyyy, E.timark, E.txtmark
order by docid desc
;

alter table ted.tmp_security add column rowtype varchar;

update ted.tmp_security set rowtype = 'title' where upper(timark) like 'TITLE%';
update ted.tmp_security set rowtype = 'title' where upper(timark) like '%DESCRIPTION%';