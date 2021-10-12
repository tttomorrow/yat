-- @testpoint: last_day函数参数为表的date类型的列
drop table if exists last_day_t001;
create table last_day_t001(
    COL_49 date
);
truncate table last_day_t001;
begin
	for i in 1..100 loop
      insert into last_day_t001 values(
          date'2020-06-17 10:00:00'
	    );
   end loop;
end;
/
select distinct last_day(COL_49) from last_day_t001;
drop table last_day_t001 CASCADE;
