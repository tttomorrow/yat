-- @testpoint: last_day函数参数为表的TIMESTAMP WITHOUT TIME ZONE 类型的列
drop table if exists last_day_t001;
create table last_day_t001(
    COL_2 TIMESTAMP WITHOUT TIME ZONE
);
truncate table last_day_t001;
begin
	for i in 1..100 loop
      insert into last_day_t001 values(
          '2001-09-28 01:00'
	    );
   end loop;
end;
/
select distinct last_day(COL_2) from last_day_t001;
drop table last_day_t001 CASCADE;
