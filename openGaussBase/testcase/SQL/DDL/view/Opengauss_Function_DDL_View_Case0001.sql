-- @testpoint: 创建视图,包括基本数据类型
--建表,使用常用基本数据类型
drop table if exists table_view_001 cascade;
create table table_view_001
(c_integer integer,
c_tinyint tinyint,
c_smallint smallint,
c_binary_integer binary_integer,
c_bigint bigint,
c_numeric numeric(10,4),
c_number number(10,4),
c_smallserial smallserial,
c_serial serial,
c_bigserial bigserial,
c_real real,
c_float float(3),
c_double_precision double precision,
c_binary_double binary_double,
c_dec dec(10,3),
c_integer1 integer(6,3),
c_money money,
c_boolean boolean,
c_char char(10),
c_varchar varchar(20),
c_varchar2 varchar2(20),
c_nvarchar2 nvarchar2(10),
c_clob clob,
c_text text,
c_name name,
c_char1 "char",
c_blob blob,
c_raw raw,
c_date date,
c_time time without time zone ,
c_time1 time with time zone,
c_time2 timestamp without time zone,
c_time3 timestamp with time zone,
c_time4 interval day(3) to second (4),
c_time5 interval year (6),
c_point point,
c_box box,
c_path path,
c_circle circle,
c_inet inet,
c_bit bit(10),
c_tsvector tsvector,
c_tsquery tsquery,
c_uuid uuid,
c_json json);
--插入数据
insert into table_view_001 values(1,10,2,5,20,123456.122331,123456.12233,default,default,default,10.365456,123456.1234,321.321,10.365456,123.123654,123.1236547,25.98,
'yes','数据库','学习数据库','设计','工程师','测试','测试呀','视图','a',empty_blob(),'deadbeef','11-20-2020','21:21:21','21:21:21 pst',
'2010-12-12','2013-12-11 pst',interval '3' day,interval '2' year, point '(2.0,0)',box '((0,0),(1,1))',path'((1,0),(0,1),(-1,0))',circle '((0,0),10)',
'192.168.1.14',b'1011111100',to_tsvector('english', 'the fat rats'),to_tsquery('fat:ab & cats'),'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11','{"f1":1,"f2":true,"f3":"hi"}');
--创建视图，添加or replace选项
create or replace view temp_view_001 as select c_integer,c_numeric, c_text from table_view_001;
--查询视图
select * from temp_view_001;
--删除视图
drop view temp_view_001;
--删表
drop table table_view_001;
