select A.tender_id as tendid, D.id as docid, extract(YEAR FROM D.datepub) as yyyy, array_agg(E.txtmark)
from ted.tender_cpv A
inner join ted.tender B on A.tender_id = B.id
inner join ted.ref_cpv C on A.cpv_code = C.code
inner join ted.tender_document D on B.id = D.tender_id
inner join ted.en_document_text E on D.id = E.doc_id
inner join ted.ref_nat_notice N on D.natnotice = N.code
where 
(A.tender_id = '2004/S 200-001512' or
A.tender_id = '2013/S 64-107835' or
A.tender_id = '2006/S 164-176883' or
A.tender_id = '2009/S 96-138431' or
A.tender_id = '2010/S 42-61080' or
A.tender_id = '2009/S 42-60742' or
A.tender_id = '2009/S 81-117107' or
A.tender_id = '2012/S 35-55891' or
A.tender_id = '2009/S 123-179878' or
A.tender_id = '2010/S 34-48883' or
A.tender_id = '2009/S 124-180731' or
A.tender_id = '2015/S 25-41562' or
A.tender_id = '2014/S 228-403278' or
A.tender_id = '2014/S 228-403253' or
A.tender_id = '2014/S 227-401711' or
A.tender_id = '2012/S 193-317422' or
A.tender_id = '2010/S 236-359899' or
A.tender_id = '2014/S 212-376026' or
A.tender_id = '2010/S 74-110930' or
A.tender_id = '2010/S 236-359899' or
A.tender_id = '2009/S 188-270992' or
A.tender_id = '2010/S 230-351085' or
A.tender_id = '2008/S 4-3504') and

	B.isocountry = 'UK' and 
	E.txtmark is not null and
	(upper(E.timark) like 'SHORT DESCRIPTION%' or
	upper(E.timark) = 'DESCRIPTION' or
	upper(E.timark) like 'TITLE%' or
	upper(E.timark) like 'TYPE OF CONTRACT%' or
	upper(E.timark) like 'ADDITIONAL%' or
	upper(E.timark) like '%CONTACT POINTS%' or
	upper(E.timark) like '%NOTICE%'
	)
	
group by tendid, docid, yyyy, E.txtmark
order by docid desc
;
