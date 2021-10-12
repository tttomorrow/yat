-- @testpoint: opengauss关键字over(非保留)，自定义数据类型名为explain，部分测试点合理报错

drop table if exists score;
create table score(
  student_id varchar(10),
  course_id varchar(10),
  score decimal(18,1)
);

insert into score values('01' , '01' , 80);
insert into score values('01' , '02' , 90);
insert into score values('01' , '03' , 99);
insert into score values('02' , '01' , 70);
insert into score values('02' , '02' , 60);
insert into score values('02' , '03' , 80);
insert into score values('03' , '01' , 80);
insert into score values('03' , '02' , 80);
insert into score values('03' , '03' , 80);
insert into score values('04' , '01' , 50);
insert into score values('04' , '02' , 30);
insert into score values('04' , '03' , 20);
insert into score values('05' , '01' , 76);
insert into score values('05' , '02' , 87);
insert into score values('06' , '01' , 31);
insert into score values('06' , '03' , 34);
insert into score values('07' , '02' , 89);
insert into score values('07' , '03' , 98);
insert into score values('08' , '02' , 89);
insert into score values('09' , '02' , 89);

SELECT course_id, score,
RANK() OVER(ORDER BY score DESC)
FROM score;

SELECT score,
ROW_NUMBER() OVER (ORDER BY score DESC)
FROM score;

SELECT score,
DENSE_RANK() OVER (ORDER BY score DESC)
FROM score;

SELECT score,
PERCENT_RANK() OVER (ORDER BY score DESC)
FROM score;

SELECT score,
CUME_DIST() OVER (ORDER BY score DESC)
FROM score;

SELECT score,
NTILE(0) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
NTILE(1) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
NTILE(20) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
NTILE(21) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
LAG(course_id,2,null) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
LEAD(course_id,2) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
FIRST_VALUE(course_id) OVER (ORDER BY score DESC)
FROM score;

SELECT score,
LAST_VALUE(course_id) OVER (ORDER BY score DESC)
FROM score;


SELECT score,
NTH_VALUE(course_id,8) OVER (ORDER BY score DESC)
FROM score;
--清理环境
drop table if exists score cascade;
