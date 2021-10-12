-- @testpoint: 用在存储过程中
drop table if exists whlp_t1;
create table whlp_t1(a int);
insert into whlp_t1 values(1);
insert into whlp_t1 values(2);
insert into whlp_t1 values(3);
commit;

begin
   for item in (select * from whlp_t1)
   loop
       raise info 'SQL%rowcount is ',sql%rowcount;
   end loop;
end;
/
drop table if exists whlp_t1;