-- @testpoint: insert组合数据类型,字符，二进制，布尔型，违法唯一约束，合理报错
-- @modify at: 2020-11-16
--建表，包含基本数据类型
drop table if exists tbl_hash;
create table tbl_hash(
col_int int,
col_integer integer,
col_BINARY_INTEGER BINARY_INTEGER,
col_smallint smallint default '7',
col_bigint bigint not null default '3',
col_real real,
col_float float,
col_BINARY_DOUBLE BINARY_DOUBLE,
col_decimal decimal,
col_number1 number,
col_number2 number(38),
col_number5 number(38,7),
col_numeric numeric,
col_char1 char(100),
col_char2 char(8000),
col_nchar1 nchar(100),
col_nchar2 nchar(8000),
col_varchar_1 varchar(100),
col_varchar_2 varchar(8000) default 'aaaabbbb',
col_varchar2_1 varchar2(100) not null default 'aaaabbbb',
col_varchar2_2 varchar2(8000),
col_nvarchar2_1 nvarchar2(100),
col_nvarchar2_2 nvarchar2(8000),
col_clob clob,
col_text text,
col_binary1 varchar2(100),
col_binary2 varchar2(8000),
col_varbinary1 varchar2(100),
col_varbinary2 varchar2(8000),
col_raw1 raw(100),
col_raw2 raw(8000),
col_blob blob,
col_date date not null default '2018-01-07 08:08:08',
col_timestamp1 timestamp ,
col_timestamp2 timestamp(6),
col_bool bool,
col_boolean boolean,
col_interval1 INTERVAL YEAR TO MONTH,
col_interval2 INTERVAL DAY TO SECOND
);
--创建索引并指定一列转为大写
drop index if exists idx_tbl_hash_3;
create unique index idx_tbl_hash_3 on tbl_hash(upper(col_nvarchar2_1),col_raw1,col_char1,col_nchar1,col_bool);
--插入数据
insert into tbl_hash(col_nvarchar2_1,col_raw1,col_char1,col_nchar1,col_bool)
--查询
select * from tbl_hash;
--再次插入同样数据，合理报错
insert into tbl_hash(col_nvarchar2_1,col_raw1,col_char1,col_nchar1,col_bool)
--删除表
drop table if exists tbl_hash cascade;



