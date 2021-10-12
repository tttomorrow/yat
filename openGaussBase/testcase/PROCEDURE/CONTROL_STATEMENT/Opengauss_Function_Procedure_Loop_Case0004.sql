-- @testpoint: forall批量查询语句

create table hdfs_t1 (
  title number(6),
  did varchar2(20),
  data_peroid varchar2(25),
  kind varchar2(25),
  interval varchar2(20),
  time date,
  ismodified varchar2(10)
);

insert into hdfs_t1 values( 8, 'donald', 'oconnell', 'doconnel', '650.507.9833', to_date('21-06-1999', 'dd-mm-yyyy'), 'sh_clerk' );

create or replace procedure proc_forall()
as
begin
    forall i in 100..120
        update hdfs_t1 set title = title + 100*i;
end;
/

call proc_forall();
select * from hdfs_t1 where title between 100 and 120;

drop procedure proc_forall;
drop table hdfs_t1;
