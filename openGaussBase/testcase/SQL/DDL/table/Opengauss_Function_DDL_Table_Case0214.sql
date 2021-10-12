-- @testpoint: create table时复制表结构中一字段类型

DROP TABLE IF EXISTS s_ord;
CREATE TABLE s_ord
(id                      NUMBER(7)
   CONSTRAINT s_ord_id_nn NOT NULL,
 customer_id             NUMBER(7)
   CONSTRAINT s_ord_customer_id_nn NOT NULL,
 date_ordered               DATE,
 date_shipped               DATE,
 sales_rep_id            NUMBER(7),
 total                      NUMBER(11, 2),
 payment_type               VARCHAR2(6),
 order_filled               VARCHAR2(1)
    );
INSERT INTO s_ord VALUES(0, 4,to_date('1993-03-26', 'yyyy-mm-dd'), to_date('2200-09-28', 'yyyy-mm-dd'), 11,
    601100, 'credit',  'Y');

drop table if exists older;
create table older as select payment_type as typed from s_ord;
select * from older;
DROP TABLE IF EXISTS s_ord;
drop table if exists older;