select A.tender_id as tendid, D.id as docid, extract(YEAR FROM D.datepub) as yyyy, array_agg(E.txtmark), array_agg(C.en)
from ted.tender_cpv A
inner join ted.tender B on A.tender_id = B.id
inner join ted.ref_cpv C on A.cpv_code = C.code
inner join ted.tender_document D on B.id = D.tender_id
inner join ted.en_document_text E on D.id = E.doc_id
inner join ted.ref_nat_notice N on D.natnotice = N.code
where 
	B.isocountry = 'UK' and 
	E.txtmark is not null and
	E.txtmark like '%ATOS%' and
	(upper(E.timark) like 'SHORT DESCRIPTION%' or
	upper(E.timark) = 'DESCRIPTION' or
	upper(E.timark) like 'TITLE')
	
group by tendid, docid, yyyy, E.txtmark, C.en
order by docid desc
;
