-- @testpoint: 与WHERE联用
drop table if exists t_ascii;
create table t_ascii(id int,v_char varchar(10));
insert into t_ascii values(1,'a');
insert into t_ascii values(2,'b');
insert into t_ascii values(3,'c');
insert into t_ascii values(4,'A');
insert into t_ascii values(5,'A');
select id,v_char from t_ascii where ascii(v_char) in (97,98) order by id;
drop table if exists t_ascii;