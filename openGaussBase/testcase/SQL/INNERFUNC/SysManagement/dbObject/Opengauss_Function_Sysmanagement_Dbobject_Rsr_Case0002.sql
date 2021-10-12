-- @testpoint: pg_relation_size(relation regclass)函数的异常校验，合理报错


-- 表、索引

CREATE TABLE customer_t1
(
    c_customer_sk             integer,
    c_customer_id             char(5)
);

select pg_relation_size();

CREATE UNIQUE INDEX index1 ON customer_t1(c_customer_sk);
insert into customer_t1 values(9,'hhh');
select pg_relation_size(regclass);


select pg_relation_size('customer_t1','customer_t1'::regclass);
select pg_relation_size('');
select pg_relation_size('*&^&%^');

drop table customer_t1;