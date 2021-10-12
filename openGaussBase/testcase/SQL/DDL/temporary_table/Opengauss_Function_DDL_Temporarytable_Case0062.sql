-- @testpoint: 创建本地临时表，指定参数ON COMMIT DELETE ROWS，进行commit后，查表无数据
-- @modify at: 2020-11-24
--开启事务
start transaction;
--建表
drop table if exists temp_table_062;
create  temporary table temp_table_062
(c_id int,
c_d_id int NOT NULL,
c_w_id int NOT NULL,
c_first varchar(16) NOT NULL,
c_middle char(2),
c_last varchar(16) NOT NULL,
c_street_1 varchar(20) NOT NULL,
c_street_2 varchar(20),
c_city varchar(20) NOT NULL,
c_state char(2) NOT NULL,
c_zip char(9) NOT NULL,
c_phone char(16) NOT NULL,
c_since date,
c_credit char(2) NOT NULL,
c_credit_lim numeric(12,2),
c_discount numeric(4,4),
c_balance numeric(12,2),
c_ytd_payment real NOT NULL,
c_payment_cnt number NOT NULL,
c_delivery_cnt bool NOT NULL,
c_end date NOT NULL,
c_data clob,
c_text blob,
c_clob clob)ON COMMIT DELETE ROWS;
--插入数据
insert into temp_table_062 values(1, 2,3,'n' ,'xx','dd','v1','cc','d2','4','r4','yt','2018-10-10','5',null,null,null,0, '90',1,'2018-10-10','vv','23','bb');
--查询,表有数据
select * from temp_table_062;
--提交事务
commit;
--查询,表无数据
select * from temp_table_062;
--删表
drop table temp_table_062;
