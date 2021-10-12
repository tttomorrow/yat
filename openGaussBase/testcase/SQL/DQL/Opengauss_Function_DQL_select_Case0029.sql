-- @testpoint: DQL语法，结合SELECT...having

drop table if exists select_test_tab;
create table select_test_tab(id number,name varchar2(30),age number);
insert into select_test_tab values(1,'aaa',10);
insert into select_test_tab values(2,'bbb',12);
insert into select_test_tab values(3,'ccc',14);
insert into select_test_tab values(4,'ddd',16);
insert into select_test_tab values(1,'eee',18);
insert into select_test_tab values(1,'adc',20);
insert into select_test_tab values(1,'abc',21);
insert into select_test_tab values(2,'eea',22);
insert into select_test_tab values(2,'eae',24);
insert into select_test_tab values(3,'ede',26);
insert into select_test_tab values(3,'aee',28);
insert into select_test_tab values(4,'cee',25);
insert into select_test_tab values(4,'gee',22);
insert into select_test_tab values(5,'fee',21);
insert into select_test_tab values(5,'iee',28);
select id,count(id) from select_test_tab where age>18 group by id having count(id)>1 order by 1,2;
drop table if exists select_test_tab;