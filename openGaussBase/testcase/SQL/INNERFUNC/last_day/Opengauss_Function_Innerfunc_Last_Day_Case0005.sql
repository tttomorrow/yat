-- @testpoint: last_day函数参数为表的数值类型列，合理报错
drop table if exists last_day_t001;
create table last_day_t001(
COL_1 bigint,
COL_4 decimal,
COL_8 double precision,
COL_13 real ,
COL_14 numeric
);
truncate table last_day_t001;
begin
	for i in 1..100 loop
      insert into last_day_t001 values(
	    fun_seq.nextval,
	    3.1415926+fun_seq.nextval,
	    3.1415926+fun_seq.nextval,
	    i/4
	    );
   end loop;
end;
/
--SELECT * from last_day_t001 LIMIT 1,10;
select distinct last_day(COL_1) from last_day_t001;
select distinct last_day(COL_4) from last_day_t001;
select distinct last_day(COL_8) from last_day_t001;
select distinct last_day(COL_13) from last_day_t001;
select distinct last_day(COL_14) from last_day_t001;
drop table last_day_t001 CASCADE;
