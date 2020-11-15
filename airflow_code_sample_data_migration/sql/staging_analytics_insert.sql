
--- Analytics Address table

CREATE TABLE public.address_analytic(
    account_id integer,
    address_1 text,
    city text,
    state text,
    zip text
);


INSERT INTO public.address_analytic(account_id, address_1, city, state,zip)
    SELECT account_id, line1 as address_1, left(line2, strpos(line2, ',') - 1) as city,
LEFT(split_part(line2, ',', 2),3) as state,
CASE WHEN (RIGHT(line2, 5) SIMILAR TO '[0-9]+')
THEN RIGHT(line2, 5) else NULL end as zip FROM public.address;


--- Analytics Account Table
create table public.account_analytics as select id,name, account_number,status from public.account;


--- Analytics Statement Table
create table public.statement_analytics as select * from public.statement;
