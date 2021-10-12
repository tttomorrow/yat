--  @testpoint: --创建 NOT NULL约束，区别大小写
delete from false_2 where a is null;
alter table false_2 add constraint cc check(a is not null);
alter table false_2 add constraint CC check(A is not null);
alter table false_2 add constraint DD check(B is not null);
alter table false_2 add constraint DD check(b is not null);