-- @testpoint: last_day函数用在join on条件中，三张表做连接
drop table if exists last_day_t001;
drop table if exists last_day_t002;
drop table if exists last_day_t003;
create table last_day_t001(
    COL_2 TIMESTAMP WITHOUT TIME ZONE,
    COL_49 date,
    COL_57 smalldatetime
);
create table last_day_t002(
    COL_2 TIMESTAMP WITHOUT TIME ZONE,
    COL_49 date,
    COL_57 smalldatetime
);
create table last_day_t003(
    COL_2 TIMESTAMP WITHOUT TIME ZONE,
    COL_49 date,
    COL_57 smalldatetime
);
truncate table last_day_t001;
truncate table last_day_t002;
truncate table last_day_t003;
begin
	for i in 1..100 loop
      insert into last_day_t001 values(
          '2001-09-28 01:00:00',
          date '2000-06-17 10:00:00',
          '2003-04-12 04:05:06'
	    );
   end loop;
   for i in 1..100 loop
     insert into last_day_t002 values(
          '2001-09-28 01:00:00',
          date '2000-06-17 10:00:00',
          '2003-04-12 04:05:06'
	    );
   end loop;
   for i in 1..100 loop
     insert into last_day_t003 values(
          '2001-09-28 01:00:00',
          date '2000-06-17 10:00:00',
          '2003-04-12 04:05:06'
	    );
   end loop;
end;
/
select last_day(t1.COL_2),last_day(t2.COL_49),last_day(t3.COL_57)
from last_day_t001 t1
join last_day_t002 t2 on t1.COL_2=t2.COL_2
join last_day_t003 t3 on last_day(t2.COL_49)=last_day(t3.COL_49)
limit 1,3;
drop table last_day_t001 CASCADE;
drop table last_day_t002 CASCADE;
drop table last_day_t003 CASCADE;
