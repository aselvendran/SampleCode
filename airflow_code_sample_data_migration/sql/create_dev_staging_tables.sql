
--- Dev Address table

CREATE TABLE public.address(
    account_id integer,
    address_1 text,
    city text,
    state text,
    zip text
);


--- Dev Account table


CREATE TABLE public.account (
    id integer,
    name text,
    encrypted_username text,
    encrypted_password text,
    account_number text,
    status text
);

--- Dev Statement table

CREATE TABLE public.statement (
    id integer,
    account_id integer,
    start_date date,
    end_date date,
    usage integer,
    charges money,
    status text
);