
CREATE TABLE user (
	id varchar NOT NULL,
	first_name varchar NOT NULL,
	last_name varchar NOT NULL,
	phone_number varchar NOT NULL,
	address varchar NOT NULL,
	pin varchar NOT NULL,
	balance int4 NULL,
	created_date timestamp NULL,
	CONSTRAINT user_phone_number_key UNIQUE (phone_number),
	CONSTRAINT user_pkey PRIMARY KEY (id)
);

CREATE TABLE transaction (
	id varchar NOT NULL,
	user_id varchar NOT NULL,
	amount int4 NOT NULL,
	remarks varchar NULL,
	transaction_type varchar NOT NULL,
	created_date timestamp NULL,
	CONSTRAINT transaction_pkey PRIMARY KEY (id)
);


-- public."transaction" foreign keys

ALTER TABLE public."transaction" ADD CONSTRAINT transaction_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);