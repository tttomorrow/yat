-- @testpoint:行存表建立,数据插入，数据查询；
drop table if exists column_store_table_datatype_02;
CREATE  TABLE column_store_table_datatype_02 (
	c0 smallint,
	c1 integer,
	c2 bigint,
	c3 decimal,
	c4 numeric,
	c5 real,
	c6 double precision,
	c7 smallserial,
	c8 serial,
	c9 bigserial,
	c10 money,
	c11 varchar(200),
	c12 char(320),
	c13 char,
	c14 text,
	c15 nvarchar2,
	c16 timestamp with time zone,
	c17 timestamp without time zone,
	c18 date,
	c19 time without time zone,
	c20 time with time zone,
	c21 interval,
	c22 clob
)
WITH (orientation=row, compression=no);
insert into column_store_table_datatype_02 values (1,2,3,1,1,1,1,1,1,1,1,'1','1','1','1','1',date'2020-08-05',date'2020-08-05',date'2020-08-05',date'2020-08-05','21:21:21 pst',interval '2' year,'1');
select * from column_store_table_datatype_02;
drop table if exists column_store_table_datatype_02;
