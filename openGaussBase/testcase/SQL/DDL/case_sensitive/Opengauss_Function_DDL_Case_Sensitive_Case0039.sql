--  @testpoint: 删除 NOT NULL约束，区别大小写
alter table false_2 drop constraint cc;
alter table false_2 drop constraint CC;
alter table false_2 drop constraint dd;
alter table false_2 drop constraint DD;