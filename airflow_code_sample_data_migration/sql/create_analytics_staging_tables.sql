
--- Analytics Address table

CREATE TABLE public.address(
    account_id integer,
    address_1 text,
    city text,
    state text,
    zip text
);


--- Analytics Account table

CREATE TABLE public.account(
    id integer,
    name text,
    account_number text,
    status text

);


--- Analytics Statement table

CREATE TABLE public.statement (
    id integer,
    account_id integer,
    start_date date,
    end_date date,
    usage integer,
    charges money,
    status text
);