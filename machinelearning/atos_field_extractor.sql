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
A.tender_id = '2008/S 4-3504' or
A.tender_id = '2009/S 243-347717' or
A.tender_id = '2014/S 191-337628' or
A.tender_id = '2012/S 95-157414' or
A.tender_id = '2012/S 51-083453' or
A.tender_id = '2012/S 201-330100' or
A.tender_id = '2011/S 137-228032' or
A.tender_id = '2012/S 193-317070' or
A.tender_id = '2010/S 44-065205' or
A.tender_id = '2011/S 188-306383' or
A.tender_id = '2008/S 252-338310' or
A.tender_id = '2009/S 210-301371' or
A.tender_id = '2014/S 91-159107' or
A.tender_id = '2006/S 152-164541' or
A.tender_id = '2009/S 49-071129' or
A.tender_id = '2010/S 187-285348' or
A.tender_id = '2010/S 187-285347' or
A.tender_id = '2009/S 122-178197' or
A.tender_id = '2011/S 140-233025' or
A.tender_id = '2013/S 155-270951' or
A.tender_id = '2013/S 155-270934' or
A.tender_id = '2014/S 149-268633' or
A.tender_id = '2013/S 104-177971' or
A.tender_id = '2010/S 174-265639' or
A.tender_id = '2012/S 101-168489' or
A.tender_id = '2011/S 154-255728' or
A.tender_id = '2009/S 174-250807' or
A.tender_id = '2009/S 74-107669' or
A.tender_id = '2014/S 130-232848' or
A.tender_id = '2008/S 126-168287' or
A.tender_id = '2011/S 224-363697' or
A.tender_id = '2010/S 207-316550' or
A.tender_id = '2007/S 180-220493' or
A.tender_id = '2011/S 111-182667' or
A.tender_id = '2010/S 209-319897' or
A.tender_id = '2012/S 103-172100' or
A.tender_id = '2011/S 157-260530' or
A.tender_id = '2014/S 97-170185' or
A.tender_id = '2009/S 197-283362' or
A.tender_id = '2012/S 28-045456' or
A.tender_id = '2012/S 43-070636' or
A.tender_id = '2010/S 134-206643' or
A.tender_id = '2010/S 211-323381' or
A.tender_id = '2013/S 242-420780' or
A.tender_id = '2008/S 128-170369' or
A.tender_id = '2008/S 91-122993' or
A.tender_id = '2010/S 59-088049' or
A.tender_id = '2014/S 66-113299' or
A.tender_id = '2008/S 78-105072') and

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
