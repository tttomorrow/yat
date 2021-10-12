-- @testpoint: last_day函数参数为表的 TIMESTAMP 类型的列
drop table if exists last_day_t001;
create table last_day_t001(
    COL_31 TIMESTAMP
);
truncate table last_day_t001;
begin
	for i in 1..100 loop
      insert into last_day_t001 values(
          to_timestamp('2020-06-17 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF')
	    );
   end loop;
end;
/
select distinct last_day(COL_31) from last_day_t001;
drop table last_day_t001 CASCADE;
