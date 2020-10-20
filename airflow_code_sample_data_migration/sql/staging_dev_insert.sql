

--- Dev Address table

create table public.address_dev as select * from public.address_analytic;

--- Dev Account table

CREATE EXTENSION pgcrypto;
create table public.account_dev as select id,name,PGP_SYM_ENCRYPT(encrypted_username,'AES_KEY') as encrypted_username,PGP_SYM_ENCRYPT(encrypted_password,'AES_KEY') as encrypted_password,account_number, status from public.account;


--- Dev Statement table

create table public.statement_dev as select * from public.statement WHERE start_date > '2018-01-01';

