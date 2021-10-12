--  @testpoint: --创建UNIQUE约束区别大小写
drop table if exists false_2 cascade;
create table false_2(a int,b int);

insert into false_2 values(1,2),(2,3),(3,4),(4,5);
alter table false_2 drop constraint yy;
alter table false_2 add constraint yy unique(a);
alter table false_2 add constraint YY unique(A);
alter table false_2 add constraint zz unique(B);
alter table false_2 add constraint zz unique(b);

alter table false_2 drop constraint yy;
alter table false_2 drop constraint YY;
alter table false_2 drop constraint ZZ;
alter table false_2 drop constraint zZ;
alter table false_2 drop constraint zz;